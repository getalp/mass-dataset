#!/usr/env/bin python
# -*- encoding: utf8 -*-

import os
import os.path as osp
import numpy as np
from collections import defaultdict
from pprint import pprint
import pydub
import shutil
import requests
from lxml import etree
from multiprocessing import Pool
import glob
import sys

# HANDLE AUDIO

def from_mp3(mp3_file_path):
    return pydub.AudioSegment.from_mp3(mp3_file_path)

def mp3_to_wav_file(mp3, output_dir=None):
    if output_dir == None:
        output_dir = get_path(mp3)
    sound = from_mp3(mp3)
    sound = sound.set_channels(1)
    sound.export(os.path.join(output_dir, get_filename(mp3))+'_one_channel.wav', format="wav")

def wav_one_channel(wav_file, output_dir=None):
    if output_dir == None:
        output_dir = get_path(wav_file)

    sound = pydub.AudioSegment.from_wav(wav_file)
    sound = sound.set_channels(1)
    sound.export(os.path.join(output_dir, get_filename(wav_file))+'_one_channel.wav', format="wav")

# PATH UTILS

def get_path(path):
    return os.path.split(path)[0]

def get_filename(path):
    return os.path.splitext(os.path.basename(path))[0]


# MAIN

outpath = sys.argv[1]
audio_ext = sys.argv[2]
text_ext = sys.argv[3]
lang = sys.argv[4] #r'eng-US'

def do_job(tasks_to_accomplish):

    # log function
    def write_log(caption_name, stage):
        with open(osp.join(outpath, 'alignment_log.txt'), 'a') as log_file:
            log_file.write('{}\t{}\n'.format(caption_name, stage))

    index_caption, caption_name = tasks_to_accomplish
    pid = os.getpid()

    if not os.path.exists(osp.join(outpath, './{}.TextGrid'.format(caption_name))):
        if audio_ext == 'mp3':
            mp3_to_wav_file(osp.join(outpath,'{}.mp3'.format(caption_name)),outpath)
        if audio_ext == 'wav':
            wav_one_channel(osp.join(outpath,'{}.wav'.format(caption_name)),outpath)
        
        if text_ext != 'txt' and os.path.exists(osp.join(outpath,'{}.{}'.format(caption_name, text_ext))):
            pre, ext = os.path.splitext(osp.join(outpath,'{}.{}'.format(caption_name, text_ext)))
            os.rename(osp.join(outpath,'{}.{}'.format(caption_name, text_ext)), pre + '.txt')
        
        #print(caption_name)
        
        # build request
        url = 'https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic'
        data = {r'LANGUAGE': lang, r'OUTFORMAT': r'TextGrid'}
        files = {r'TEXT': open(osp.join(outpath, '{}.txt'.format(caption_name)), 'rb'),
                 r'SIGNAL': open(osp.join(outpath, '{}_one_channel.wav'.format(caption_name)), 'rb')}
        #print('Sending request ...')
        r = requests.post(url, files=files, data=data)
        #print('Processing results ...')

        if r.status_code == 200:
            root = etree.fromstring(r.text)
            success = root.find('success').text
            download_url = root.find('downloadLink').text

            if success != 'false':
                request_download = requests.get(download_url, stream=True)
                if request_download.status_code == 200:
                    try:
                        with open(osp.join(outpath, '{}.TextGrid'.format(caption_name)), 'wb') as f:
                            f.write(request_download.content)
                        print('{} [{}]: {} OK'.format(pid, index_caption, caption_name))
                    except:
                        write_log(caption_name, 'FAIL Write TextGrid')
                        print('{} [{}]: {} FAIL Write TextGrid'.format(pid, index_caption, caption_name))
                        pass
                else:
                    write_log(caption_name, 'FAIL Download TextGrid')
                    print('{} [{}]: {} FAIL Download TextGrid'.format(pid, index_caption, caption_name))
            else:
                write_log(caption_name, 'FAIL Alignment')
                print(r.text)
                print('{} [{}]: {} FAIL Alignment'.format(pid, index_caption, caption_name))
        else:
            write_log(caption_name, 'FAIL Alignment Request')
            print('{} [{}]: {} FAIL Alignment Request'.format(pid, index_caption, caption_name))

        # delete temp files
        #os.remove(osp.join(outpath, '{}.{}'.format(caption_name, text_ext)))
        #os.remove(osp.join(outpath, '{}.{}'.format(caption_name, audio_ext)))

    else:
        print('{} [{}]: {} SKIP'.format(pid, index_caption, caption_name))


def main():
    # get captions belonging to the test set
    file_list = [x for x in map(get_filename, glob.glob(osp.join(outpath, '*.{}'.format(audio_ext)))) if x.find('_one_channel')==-1]
    number_of_processes = min(int(sys.argv[5]),16)
    tasks_to_accomplish = []

    for index_file, file_name in enumerate(file_list, 1):
        tasks_to_accomplish.append((index_file, file_name))

    p = Pool(number_of_processes)
    p.map(do_job, tasks_to_accomplish)

if __name__ == '__main__':
    """
    Script used to force align the spoken version of the Bible with its transcription using Maus Forced Aligner

    As we already provide the forced alignments, please use this script only if necessary.
    WebMaus should be warned before sending huge amounts of files to be aligned (see WebMaus' Terms: https://clarin.phonetik.uni-muenchen.de/BASWebServices/help)

    This scripts expects the following arguments:
        <input_folder>: path to the folder containing the audio files (either MP3 or WAV) and their transcriptions (either TXT or LAB)
        <audio_ext>: extension of the audio files (MP3 or WAV). Audio files will be converted to one-channel WAV (regardless of the input format)
        <text_ext>: extension of the transcription files (TXT or LAB)
        <language_code>: (ISO 639-3 - ISO 3166-1 | e.g. American English: eng-US)>
        <num_jobs>: number of threads to use
    """

    if len(sys.argv) < 5:
        print("USAGE: python2.7 align.py <input_folder> <audio_ext> <text_ext> <language_code (ISO 639-3 - ISO 3166-1 | e.g. American English: eng-US)> <num_jobs>")
        sys.exit(1)

    print('\n\n{}\nUsing the following parameters:\n{} \
           \n\tSource folder: {}\
           \n\tAudio format: {}\
           \n\tText format: {}\
           \n\tLanguage: {}\
           \n\tJobs: {}\
         \n{}'.format('*'*50, '-'*50,
                      sys.argv[1], #outpath
                      sys.argv[2], #audio_ext
                      sys.argv[3], #text_ext
                      sys.argv[4], #lang
                      min(int(sys.argv[5]),16),
                      '*'*50))
    main()

