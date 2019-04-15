# -*- encoding: utf8 -*-
#Collection of supporting functions for the coupe_verset audio slicer
#2.0v 15/04/2019 MZ BOITO

import glob, os, codecs
from praatio import tgio
from pprint import pprint

class Element():
    def __init__ (self, text_key, key, interval):
        self.text_key = text_key
        self.key = key
        self.interval = interval

    def to_string(self):
        return " ".join([self.text_key, str(self.interval.start), str(self.interval.end)])
    
    def _shift_interval(self, interval, value):
        if (interval.start - value) < 0 or (interval.end - value) < 0:
            raise Exception("Invalid value for shift interval function")
        return tgio.Interval(format_number(interval.start - value), format_number(interval.end - value), interval.label)

class TextgridWord(Element):
    def __init__(self, text_key, key, graphemic, phonetic, phones_list):
        Element.__init__(self, text_key, key, graphemic)
        self.graphemic = self.interval
        self.phonetic = phonetic
        self.phones_list = phones_list

    def shift_interval(self, value):
        self.interval = self._shift_interval(self.interval, value)
        self.graphemic = self.interval
        self.phonetic = self._shift_interval(self.phonetic, value)
        self.phones_list = [self._shift_interval(element, value) for element in self.phones_list]

class TextgridSilence(Element):
    def __init__(self, text_key, key, interval):
        Element.__init__(self, text_key, key, interval)

    def shift_interval(self, value):
        self.interval = self._shift_interval(self.interval, value)

def get_files_list(path):
    return glob.glob(path + "/*")

def get_prefix(file_name):
    return file_name.split("/")[-1].split(".")[0]

def shift_intervals(texgrid_list, value):
    for word_obj in texgrid_list:
        word_obj.shift_interval(value)

def create_textgrid_obj(textgrid_list):
    new_dict = dict()
    keys = ["ORT", "KAN", "MAU"]
    for key in keys:
        new_dict[key] = tgio.TextgridTier(key, [], 0.0, textgrid_list[-1].interval.end)
        new_dict[key].tierType = tgio.INTERVAL_TIER

    for element in textgrid_list: 
        new_dict["ORT"].entryList.append(element.interval)
        try:
            phonetic = element.phonetic
            phones_list = element.phones_list
        except AttributeError:
            phonetic = element.interval
            phones_list = [element.interval]
    
        new_dict["KAN"].entryList.append(phonetic)
        new_dict["MAU"].entryList += phones_list

    textgrid_obj = tgio.Textgrid()
    for key in keys:
        textgrid_obj.addTier(new_dict[key])


    return textgrid_obj

def print_elements_dictionary(elements_dictionary, key):
    for element in elements_dictionary[key]:
        print(element.to_string())

def format_number(float_number):
    return float("{:.2f}".format(float_number))

def elements_counter(elements_dictionary):
    sil = 0
    words = 0
    for element_list in elements_dictionary.values():
        for element in element_list:
            try:
                element.graphemic
                words +=1
            except AttributeError:
                sil +=1
    return words, sil

def create_log_file(file_name, dictionary_sequence, textgrid_text):
    with codecs.open(file_name, "w","utf-8") as log:
        log.write("{}\t{}\n".format(len(dictionary_sequence.split(" ")), len(textgrid_text.split(" ")) ) )
        try:
            for i in range(len(dictionary_sequence.split(" "))):
                log.write("\t".join([dictionary_sequence.split(" ")[i], textgrid_text.split(" ")[i]]) + "\n")
        except Exception:
            pass

def check_root(root_directory):
    try:
        os.stat(root_directory)
    except:
        os.makedirs(root_directory)