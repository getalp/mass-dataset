# Audio Slicer

## RUNNING
~~~~
python3 coupe_verset.py --lab <CHAPTER TEXT> --textgrid <TEXGRID> --wav <WAV FILES> --output <OUTPUT FOLDER> --language <LANGUAGE ID> --force --verbose
~~~~

## PARAMETERS

**--lab**: the folder containing the chapters text files **(with verse information)** available at dataset/LANGUAGE/raw_txt/ or extracted from the [website](https://www.faithcomesbyhearing.com/audio-bibles/bible-recordings)

**--textgrid**: the folder containing the output of the alignment **(without verse information)**

**--wav**: the folder containing the audios, such as downloaded from bible.is 

**--language**: Language IDs (config.py). Current covered languages:
     en : English
     es : Spanish
     eu : Basque
     fi : Finnish
     fr : French
     hu : Hungarian
     ro : Romanian
     ru : Russian

**--force**: right now the script only works with this option on. If you want to extend the audio slicer by allowing imperfect alignments, you can start by removing this argument; (check DEBUG AND ETC below)

**--verbose**: if you like having a lot of textual output. :)

## DEPENDENCIES

* *Multiprocessing*: The multiprocessing library is used. If not supported by the machine, it can be simply replaced by removing the commentary on the process function (coupe_verset.py).

* *praatio*: necessary to process the textgrid input

* *sox*: is used for slicing the audios. If not executed on a linux machine, this command needs to be replaced on the slice_audio function (coupe_verset.py).

**/!\ THIS IS A PYTHON 3.5v IMPLEMENTATION.**

## DEBUG AND EXTENSIONS

**NAME EXTENSIONS:** Please note that the script makes some assumptions about file names and extensions. All of these are listed on config.py

**ERROR LOG:** In case of exception, the script generates a log file. This log file is called FILE_ID_error_log and it prints the generated alignment, element by element, allowing debug.

**EXTENSION:** Perfect alignment was generated through an iterative process of failed alignment generation and inclusion of new regular expressions in the clean function (parser.py) for each one of the covered languages. By adding cases for new languages, the script can be easily extended to new languages.

**IMPEFECT ALIGNMENT:** We include the imperfect_raw_grid_align function that allows impefect alignment between chapter text and textgrid. Please check that function at coupe_verset.py for more details. 

