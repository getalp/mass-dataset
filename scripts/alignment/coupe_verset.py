# -*- encoding: utf8 -*-
# 2.0v last modified the 15/09/2019 MZ BOITO

import os, sys, codecs, argparse
from praatio import tgio
from pprint import pprint
from multiprocessing import Process
from utils import *
from parser import *
from config import langs, TEXTGRID_SUFFIX, WAV_SUFFIX, SIL_KEY, SEP_STR


def imperfect_raw_grid_align(dictionary_sequence, textgrid_sequence, verbose=False):
    
    '''
    /!\ ALLOWING NOT PERFECT ALIGNMENTS 
    remove "imperfect_" from the function name and comment (or remove) the raw_grid_align function
    add the following imports at the beginning of this script:

    from alignment.sequence import Sequence
    from alignment.vocabulary import Vocabulary
    from alignment.sequencealigner import SimpleScoring, GlobalSequenceAligner

    /!\ DO NOT USE THE --force option with this function
    You might need to remove some asserts (and have some headaches) to make this option work
    We do not advise using it
    '''
    a = Sequence(dictionary_sequence.split()) #dictionary
    b = Sequence(textgrid_sequence.split()) #textgrid
    v = Vocabulary()
    aEncoded = v.encodeSequence(a)
    bEncoded = v.encodeSequence(b)
    # Create a scoring and align the sequences using global aligner.
    scoring = SimpleScoring(2, -1)
    aligner = GlobalSequenceAligner(scoring, -2)
    _, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)

    if not encodeds:
        raise Exception("Alignment Module failed")
    
    # Iterate over optimal alignments, print them if verbose
    for encoded in encodeds:
        alignment = v.decodeSequenceAlignment(encoded)
        if verbose:
            for tup in list(alignment):
                print(tup)
            print ('Alignment score:', alignment.score)
            print ('Percent identity:', alignment.percentIdentity())
    return alignment

def raw_grid_align(dictionary_sequence, textgrid_sequence, verbose=False):
    '''
    This function considers perfect textual alignment between chapter 
    raw text and textgrid (after parser.py cleaning). If not the case, 
    please check the README and imperfect_raw_grid_alignment for more 
    information.
    '''
    dictionary_sequence = dictionary_sequence.split(" ")
    textgrid_sequence = textgrid_sequence.split(" ")
    alignment = list()
    for i in range(len(textgrid_sequence)):
        alignment.append((dictionary_sequence[i], textgrid_sequence[i]))
    return alignment

def get_tier_by_interval(start, end, tier_dictionary):
    return [element for element in tier_dictionary.entryList if element.start >= start and element.end <= end]

def get_key_by_index(dictionary, index):
    keys = list(dictionary.keys())
    key_index = 0
    while(index >= 0 and key_index < len(keys)):
        line = dictionary[keys[key_index]].split(" ")
        l_length = len(line)
        if index >= l_length:
            index -= l_length
            key_index +=1
        else: #index < l_length, the word is at line[index], key is at keys[key_index]
            return line[index], keys[key_index]
    raise Exception("Key not found: Alignment index problem")

def add_time_windows(dictionary, textgrid, alignment):
    #ORT -> words; #KAN -> phonetic transcription; #MAU -> phoneme alignment
    richer_alignment = []
    last_verse = 0
    for i in range(len(alignment)):
        dict_word, tg_word = alignment[i]
        try:
            word, verse = get_key_by_index(dictionary, i)
            last_verse = verse
        except Exception: #didn't find the match on the dictionary, uses last alignment found
            verse = last_verse

        if args.force:
            assert word == dict_word, "Alignment mismatch between the dictionary and the textgrid"
        
        graphemic_transcription = textgrid.tierDict["ORT"].entryList[i]

        #if args.force:
        assert graphemic_transcription.label == tg_word, "Graphemic alignment mismatch"

        phonetic_transcription = get_tier_by_interval(graphemic_transcription.start, graphemic_transcription.end, textgrid.tierDict["KAN"])[0]
        phones_list = get_tier_by_interval(graphemic_transcription.start, graphemic_transcription.end, textgrid.tierDict["MAU"])
        tg_word = TextgridWord(tg_word, verse, graphemic_transcription, phonetic_transcription, phones_list)
        richer_alignment.append(tg_word)

    return richer_alignment

def merge_silence(textgrid, alignment):
    merged_list = []
    silence_list = textgrid.tierDict["ORT"].getNonEntries()
    sil_index = 0
    text_index = 0
    last_verse = 0
    while(text_index < len(alignment) or sil_index < len(silence_list)):
        if sil_index == len(silence_list): #finished with the silence
            merged_list.append(alignment[text_index])
            text_index +=1
        elif text_index == len(alignment) or alignment[text_index].graphemic.start > silence_list[sil_index].start: 
            #finished with the text or the silence comes first
            sil_obj = TextgridSilence(SIL_KEY,last_verse, silence_list[sil_index])
            merged_list.append(sil_obj)
            sil_index +=1
        else: #word comes first
            merged_list.append(alignment[text_index])
            last_verse = alignment[text_index].key
            text_index +=1
    return merged_list

def split_by_verse(alignment):
    dictionary = dict()
    for element in alignment:
        try:
            dictionary[element.key].append(element)
        except KeyError:
            dictionary[element.key] = [element]
    return dictionary

def split_silence(silence_object):
    old_interval = silence_object.interval
    new_ending = format_number((old_interval.start + (old_interval.end - old_interval.start)/2.0))
    new_interval = tgio.Interval(old_interval.start, new_ending, old_interval.label)
    new_obj = TextgridSilence(silence_object.text_key, silence_object.key, new_interval)
    new_interval = tgio.Interval(new_ending, old_interval.end, old_interval.label)
    carry = TextgridSilence(silence_object.text_key, -1, new_interval)
    return new_obj, carry

def split_boundary_silence(alignment_dictionary):
    new_dictionary = dict()
    keys = list(alignment_dictionary.keys())
    carry = None
    for key in keys:
        if carry:
            carry.key = key
            new_dictionary[key] = [carry]
            carry = None #consumes carry
        else:
            new_dictionary[key] = []
        
        if key == keys[-1]: #last key, nothing to pass for the next 
            new_dictionary[key] += alignment_dictionary[key]
        else:
            if alignment_dictionary[key][-1].text_key == SIL_KEY: #if the verse ends with silence
                new_dictionary[key] += alignment_dictionary[key][:-1] #everything but the silence goes to the next dictionary
                new_obj, carry = split_silence(alignment_dictionary[key][-1])
                new_dictionary[key].append(new_obj)

            else: #the verse doesn't start or end with silence
                new_dictionary[key] += alignment_dictionary[key]

    return new_dictionary

def align(file, lab_dictionary, grid, verbose=False, language=None):
    dictionary_sequence = " ".join(lab_dictionary.values()) #get the text from the dictionary
    tg=tgio.openTextgrid(grid)
    
    tg.tierDict["ORT"] = clean_textgrid(tg.tierDict["ORT"], language) #remove enconding problems for alignment's sake
    entryList = tg.tierDict["ORT"].entryList    
    concatenated_ort = " ".join([entry.label for entry in entryList if entry != "­"])
    
    if args.verbose:
        print("\tDICIONARY OUTPUT")
        pprint(lab_dictionary)
        print("\tTEXTGRID OUTPUT")
        print(concatenated_ort)

    sys.setrecursionlimit(2000) #/!\ this might be a problem
    split_entry = concatenated_ort.split(" ")

    if args.force:
        try:
            assert len(dictionary_sequence.split(" ")) == len(split_entry), "Number of words mismatch between lab and textgrid"
        except AssertionError:
            create_log_file(file.split("/")[-1] + "_error_log", dictionary_sequence, concatenated_ort)
            exit(1)
        
    alignment = raw_grid_align(dictionary_sequence, concatenated_ort)
    if args.force:
        assert len(alignment) == len(dictionary_sequence.split(" ")), "Number of words mismatch between final alignment and dictionary"
    
    richer_alignment = add_time_windows(lab_dictionary, tg, alignment)
    complete_alignment = merge_silence(tg, richer_alignment)
    splitted_alignment = split_by_verse(complete_alignment)
    final_alignment = split_boundary_silence(splitted_alignment)

    words, sil = elements_counter(final_alignment)
    if verbose:
        print("Final alignment has %d words and %d silence marks" % (words, sil))
    assert words == len(alignment), "The script lost part of the words during the alignment"
    return final_alignment

def generate_audio_cuts(alignment_dictionary):
    return [(key, alignment_dictionary[key][0].interval.start, alignment_dictionary[key][-1].interval.end) for key in alignment_dictionary.keys()]

def slice_audio(audio, output_prefix, windows, verbose=False):
    if verbose:
        print("Cutting audio %s" % (audio))
    for (key, start, end) in windows:
        output_file = output_prefix + SEP_STR + str(key) + WAV_SUFFIX
        if verbose:
            print(output_file, start, end)
        os.system("sox {} {} trim {} ={}".format(audio, output_file, start, end))

def write_new_textgrids(output_prefix, windows, alignment_dictionary):
    assert len(windows) == len(alignment_dictionary.keys()), "Size Mismatch between audio windows and textgrids"
    for (key, start, _) in windows:
        if start != 0:
            shift_intervals(alignment_dictionary[key], start)
        obj = create_textgrid_obj(alignment_dictionary[key])
        output_file = output_prefix + SEP_STR + str(key) + TEXTGRID_SUFFIX
        obj.save(output_file)

def write_text_files(output_prefix, lab_dictionary):
    for key in lab_dictionary.keys():
        output_file = output_prefix + SEP_STR + str(key) + ".txt"
        with codecs.open(output_file, "w","utf-8") as output_file:
            output_file.write(lab_dictionary[key] + "\n")

def process_document(lab_file, args):
    if args.verbose:
            print(lab_file)
    file_prefix = get_prefix(lab_file)
    lab_dictionary = txt_to_dict(lab_file, args.language)
    textgrid_file = os.path.join(args.textgrid, file_prefix + TEXTGRID_SUFFIX)
    alignment_dictionary = align(lab_file, lab_dictionary, textgrid_file, language=args.language, verbose= args.verbose)
    windows = generate_audio_cuts(alignment_dictionary)
    output_prefix = os.path.join(args.output, file_prefix) 
    slice_audio(os.path.join(args.wav,  file_prefix + WAV_SUFFIX), output_prefix, windows, verbose=args.verbose)
    write_new_textgrids(output_prefix, windows, alignment_dictionary)
    write_text_files(output_prefix, lab_dictionary)

def process(args):   
    labs = get_files_list(args.lab)
    textgrids = get_files_list(args.textgrid)
    wavs = get_files_list(args.wav)

    assert len(labs) == len(textgrids) and len(textgrids) == len(wavs), "Different number of files inside the folders"

    for lab_file in labs:
        # 1) REMOVE THE COMMENT BELOW TO REMOVE MULTIPROCESSING
        process_document(lab_file, args)
        # 2) COMMENT THE FOLLOWING 3 LINES TO REMOVE MULTIPROCESSING
        #p = Process(target=process_document, args=(lab_file, args))
        #p.start()
    #p.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lab', type=str, nargs='?', help='lab folder')
    parser.add_argument('--textgrid', type=str, nargs='?', help='textgrid folder')
    parser.add_argument('--wav', type=str, nargs='?', help='wav folder')
    parser.add_argument("--verbose", "-v", help="increases output verbosity", action="store_true")
    parser.add_argument("--force", "-f", help="forces a perfect alignment between textgrid and lab", action="store_true")
    parser.add_argument('--output', type=str, nargs='?', help="name for the output folder")
    parser.add_argument('--language', type=str, nargs='?', help='specifies language for cleaning and alignment')
    args = parser.parse_args()
    if not (args.lab and args.textgrid and args.wav and args.output):
        parser.print_help()
        print("LIST OF SUPPORTED LANGUAGES: %s" % (" ".join(langs)))
        exit(1)
    check_root(args.output)
    process(args)
