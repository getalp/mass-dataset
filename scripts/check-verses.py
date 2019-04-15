# -*- encoding: utf8 -*-
import re
import subprocess
import os
from pprint import pprint
from copy import deepcopy
import itertools
import numpy as np
import glob
import sys


def add_missing_dimensions(input_list, return_labels=False):
    list_ = deepcopy(input_list)
    words = []
    redimmed_lists = []

    # grab each word in sublist
    for sublist in list_:
        words.append([dim_label for dim_label, dim_value in sublist])
    # gather words of each sublist and remove duplicates
    vocabulary = set(list(itertools.chain(*words)))
    # adds words in vocabulary in each sublist if not already in sublist
    for sublist_index, sublist in enumerate(list_):
        sublist.extend([(dim_label, 0) for dim_label in vocabulary - set(words[sublist_index])])
    # sort list alphabetically and return dim_value only (and label if necessary)
    for sublist in list_:
        if return_labels:
            redimmed_lists.append([sorted_sublist for sorted_sublist in sorted(sublist, key=lambda tup: tup[0])])
        else:
            redimmed_lists.append(np.array([dim_value for dim_label, dim_value in
                                            sorted(sublist, key=lambda tup: tup[0])]))
    return redimmed_lists


FILENAME_REGEX = re.compile(
    r"(B[0-9]{1,2}_*)([0-9]{1,2}_*[0-9]{0,1}[A-Z][a-z]*)_*([A-Z0-9]*)(_verse_[0-9]{1,2}\.TextGrid)")
NAMES = [('Matthew', 'Matthieu', 'San_Mateo', 'S_Mateus'), ('Mark', 'Marc', 'San_Marcos', 'S_Marcos'),
         ('Luke', 'Luc', 'San_Lucas', 'S_Lucas'), ('John', 'Jean', 'San_Juan', 'S_Joao'),
         ('Acts', 'Actes', 'Hechos', 'Atos'), ('Romans', 'Romains', 'Romanos'),
         ('Corinthians', 'Corinthiens', 'Corintios'), ('Galatians', 'Galates', 'Galatas'),
         ('Ephesians', 'Ephesiens', 'Efesios'), ('Philippians', 'Philippiens', 'Filipenses'),
         ('Colossians', 'Colossiens', 'Colosenses', 'Colossenses'), ('Thess', 'Thess', 'Tes', 'Tess'),
         ('Timothy', 'Timothee', 'Timoteo'), ('Titus', 'Tite', 'Tito'), ('Philemon', 'Philemon', 'Filemon'),
         ('Hebrews', 'Hebreux', 'Hebreos', 'Hebreus'), ('James', 'Jacques', 'Santiago', 'S_Tiago'),
         ('Peter', 'Pierre', 'San_Pedro', 'Pedro'), ('Jude', 'Jean', 'Judas', 'S_Judas'),
         ('Revelation', 'Apocalypse', 'Apocalipsis', 'Apocalipse')]


def list_verses():
    verseLangDict = {}
    # for each language, list all verses
    for language_dir in glob.glob(os.path.join(sys.argv[1], '*_corpus/')):
        # get language name
        dir_name = os.path.split(os.path.dirname(language_dir))[1]
        lang = dir_name.split('_')[0]
        # list verses
        verses = map(os.path.basename, glob.glob(os.path.join(language_dir, 'textgrid/*.TextGrid')))
        verse_list = []
        verse_list_original_name = []
        for verse in verses:
            # swap names
            verse_list_original_name.append(verse)
            if lang in ['french', 'spanish', 'basque', 'portuguese']:
                for name in NAMES:
                    for foreign_name in sorted(name[1:], key=lambda e: len(e), reverse=True):
                        verse = verse.replace(foreign_name, name[0])
            try:
                match_verse = re.match(FILENAME_REGEX, verse)
                book_chapter = match_verse.group(2)
                verse_number = match_verse.group(4)
                new_name = book_chapter + verse_number
                verse_list.append(new_name)
            except:
                print("WRONG FILE PATTERN: File {} for language {}\n".format(verse, lang))
        verseLangDict[lang] = {'normalised_name': verse_list,
                               'original_name': dict(zip(verse_list, verse_list_original_name))}
    return verseLangDict


def dump(verseLangDict, as_name=False):
    sorted_lang = sorted(verseLangDict.keys())
    aligned = add_missing_dimensions([[(verse, 1) for verse in verseLangDict[lang]['normalised_name']]
                                      for lang in sorted_lang], return_labels=True)
    label = [verset for verset, presence in aligned[1]]
    aligned_true = [[presence for verset, presence in lang] for lang in aligned]

    with open(os.path.join(sys.argv[1], "recap_verses-anName-{}.csv".format(as_name)), mode="w", encoding="utf8") as ficEcr:
        # write header
        header = ['ID', 'Label'] + list(sorted_lang)
        paths = ['', 'Path'] + [os.path.join(sys.argv[1], '{}_corpus/wav/'.format(lang)) for lang in sorted_lang]
        ficEcr.write(','.join(header) + "\n")
        ficEcr.write(','.join(paths) + "\n")
        # write recap
        intersection = sum([int(0 not in verset_presence) for verset_presence in zip(*aligned_true)])
        available = ['', 'Available'] + [sum(lang) for lang in aligned_true] + ['Intersection']
        missing = ['', 'Missing'] + [len(lang) - sum(lang) for lang in aligned_true] + [intersection]
        ficEcr.write(','.join(map(str, available)) + "\n" + ','.join(map(str, missing)) + "\n")

        # write details
        for row in range(0, len(label)):
            if not as_name:
                ficEcr.write(','.join([str(row), label[row]] + [str(lang[row]) for lang in aligned_true]) + "\n")
            else:
                ficEcr.write(','.join([str(row), label[row].replace('.TextGrid', '')] + [verseLangDict[sorted_lang[i_lang]]['original_name'].get(label[row], 'Not Available').replace('.TextGrid', '')
                                                                                        for i_lang, lang in enumerate(aligned_true)]) + "\n")


if __name__ == '__main__':
    """
    Generates a CSV files listing the verses available for each language.

    As not all the verses of a given language exist in another language, this CSV file can be use to 
    get a list of verses common to all languages. If a verse exists in a given language, its name (or 1) will 
    printed, 'Not Available' (or 0) otherwise. 


    Script expects the following arguments:
        <str input_folder>: path to folder containing a subfolder for each language (subfolders should have the following name pattern 'LANG_corpus')
                            each subfolder should contain a 'textgrid' folder comprising a textgrid for each verse (create by coupe_verset.py)

        <bool as_name>: if True script will print the name of verse if available in the language, or 'Not Available' if not available
                        if False ----------------[        1        ]---------------------------------[       0     ]----------------

    """
    if len(sys.argv) < 2:
        print("USAGE: python3 check_verses.py <str input_folder> <bool as_name True|False>")
        sys.exit(1)

    if len(sys.argv) >= 2:
        as_name = sys.argv[2].lower() == 'true'

    verseLangDict = list_verses()
    dump(verseLangDict, as_name)


