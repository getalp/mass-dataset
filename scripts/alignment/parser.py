# -*- encoding: utf8 -*-
#Collection of cleaning/parsing functions for the coupe_verset audio slicer
#2.0v 15/04/2019 MZ BOITO

import re, codecs

def split_lab(text, language=None):
    p_lines = []
    regexp = re.compile(r'([0-9]+-[0-9]+)')
    number_flag = False
    last_number = 0
    if language == "eu":

        if re.compile(r'[0-9]+\s*-\s*[0-9]+').search(text):
            #print(text)
            text = re.sub(r'([0-9]+)\s*-\s*([0-9]+)', r'(\1-\2)', text) 
            #text = re.sub(r'(\D)\s*-\s*(\D)')
            #print(text)
            #exit(1)

    for line in text.split("    "): #4 space
        if regexp.search(line) and language != "hu": #e.g.   (1-39)  text
            l = line.split("(")
            l1, number, l3 = l[0], l[1].split(")")[0], l[1].split(")")[1]
            number = number.split("-")[-1] #removes first part of "(START-END)"
            if int(number) > int(last_number):
                last_number = number
            if not number_flag:
                p_lines += [l1, last_number, l3]
            else: #adds the number to match transcription
                p_lines += [l1, last_number, l[1]]

        else:
            if line.replace(" ","").isdigit():
                number_flag = True
                last_number = line.replace(" ","")
            else:
                number_flag = False
            p_lines.append(line)
    return p_lines

def txt_to_dict(txt_path, language=None):
    output_dict = dict()
    last_key = 0 # zero is the key for the chapter's title
    with codecs.open(txt_path, "r", "utf-8") as txt_file:
        for line in txt_file:
            for possible_line in split_lab(line, language=language): 
                line = clean(possible_line,language=language)
                if isinstance(line, int): #verse number
                    last_key = line 
                elif line: #text from the last verse
                    output_dict[last_key] = line
    return output_dict

def remove_double_space(text, language=None):
    if language == "es":
        split_entry = text.split(" ")
        i  = 0
        while(i < len(split_entry)):
            if split_entry[i] == '\xad': #\xad is a 'soft hyphen', but due to coding problem it is printed as an invisible character
                del split_entry[i] 
            i+=1
        text = " ".join(split_entry)
    while "  " in text:
        text = text.replace("  "," ")
    return text

def clean_textgrid(dictionary_case, language):
    if language == "es" or language == "hu":
        token = '\xad' if language == "es" else '\x92'
        i  = 0
        while(i < len(dictionary_case.entryList)):
            if dictionary_case.entryList[i].label == token: 
                del dictionary_case.entryList[i]
            i+=1
    return dictionary_case

def clean(line, language=None):
    marks = ["“", "”","’"]
    punc = [".","!","?",","]

    if language == "en":
        line = re.sub(r'(\D)’s', r'\1 ’s', line) #space before the apostrophe missing 
        line = line.replace("—"," ")
        for symbol in [" ", ".", ",", "?", "!"]:
            line = line.replace(" ’ s" + symbol, " ’s" + symbol)
    elif language == "ru":
        line = line.replace("\'","").replace("--","")
    elif language == "es":
        line = line.replace("»","").replace("«","").replace("–","").replace('\xad',"")
        line = re.sub(r'(\D)¿(\D)', r'\1 ¿\2', line)
    elif language == "fr":
        line = line.replace("»","").replace("«","").replace("–","").replace('\xad',"").replace("…","")
    elif language == "eu":
        line = line.replace("»"," ").replace("«"," ").replace("—"," ").replace("-","").replace(":","").replace("/", " ").replace("…","") #« between words—
    elif language == "fi":
        line = line.replace("-","").replace("‘","").replace(":","")
    elif language == "hu":
        line = line.replace("\""," ").replace(":"," ").replace("-","").replace("\x92"," ").replace(",", " ")
    elif language == "ro":
        line = line.replace("–","").replace(":","").replace("»","").replace("…","")

    line = re.sub(r',(\D)', r', \1', line) #space missing after a comma
    line = re.sub(r'(\D)!(\D)', r'\1! \2', line) #space missing after exclamation point 
    line = re.sub(r'(\D)’(\D)', r'\1’ \2', line) #space missing after ending of a quote 
    line = re.sub(r'(\D)”(\D)', r'\1” \2', line) #space missing after ending of a quote 
    line = re.sub(r'(\D)“(\D)', r'\1 “\2', line) #space missing before beginning of a quote 

    line = line.replace("’ "," ")

    for symbol in punc + [")","(",";", "]", "["] + marks:
        line = line.replace(symbol, "")

    line = remove_double_space(line)
    line = line.replace("\t","")

    if line and line[0] == " ":
        line = line[1:]
    if line and line[-1] == " ":
        line = line[:-1]

    try:
        line = int(line) #verse
        return line
    except ValueError: #real text
        return line.strip("\n")