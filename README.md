# MaSS - Multilingual corpus of Sentence-aligned Spoken utterances

This is the repository for the CMU multilingual speech extension data set presented on the paper entitled *[MaSS: A Large and Clean Multilingual Corpus of Sentence-aligned Spoken
Utterances Extracted from the Bible](https://arxiv.org/pdf/1907.12895.pdf)*.

## Data
For copyright reasons, we are not allowed to share the audio files however, we provide the extraction pipeline below. We also highlight this pipeline can be used to new languages of interested.
Inside the dataset folder, for each language we provide:
- Alignment textgrids (from Maus forced aligner)
- Final textual output and segments textgrids
- [Mel Filterbank Spectrograms (such as used in the paper's experiments)](https://zenodo.org/record/3354711) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3354711.svg)](https://doi.org/10.5281/zenodo.3354711)


## Pipeline

### 1) Downloading audio chapters from [bible.is](bible.is).

  1.1. The audios used in our work are available in the following links:
  - [Basque dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/eus/EUSEABN1DA)
  - [English dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/eng/ENGESVN1DA)
  - [Finnish dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/fin/FIN38VN1DA)
  - [French dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/frn/FRNTLSN2DA)
  - [Hungarian dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/hun/HUNHBSN1DA)
  - [Romanian dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/ron/RONDCVN1DA)
  - [Russian dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/rus/RUSS76N2DA)
  - [Spanish dataset](https://www.faithcomesbyhearing.com/audio-bibles/download/spn/SPNBDAN1DA)

  1.2. The audios were converted from multi to single channel and forced aligned by using [this](https://github.com/getalp/mass-dataset/blob/master/scripts/force-align.py) script. 

  1.3. The raw chapter text files are not available for download anymore at the website. Thus, we provide them at dataset/LANGUAGE/raw_txt/. For new languages, chapter text files can be extracted from [this webpage](https://www.faithcomesbyhearing.com/audio-bibles/bible-recordings). 
  These .txt files (chapter level) should be put on the same folder than the audios.

### 2) Aligning the data with [Maus forced aligner](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSBasic)
For the covered languages, we make available the output from the Maus forced aligner in LANGUAGE/maus\_textgrid/. For new languages, please check the Website.

### 3) Obtaining speech alignment on a verse level
For each language, the audios were sliced in verses considering the output of 1.3. and the generated texgrids (2.). More details available [here](https://github.com/getalp/mass-dataset/blob/master/scripts/alignment/).

### 4) ID equivalence across languages
For translating the IDs in English, we provide the simple python script below.

~~~~
python3 scripts/fetch_data.py <language folder> <output folder> <language code>
~~~~

### 5) Generate a CSV file listing the verses available for each language

Use [this](https://github.com/getalp/mass-dataset/blob/master/scripts/check-verses.py) script to tenerate a CSV files listing the verses available for each language.
As not all the verses of a given language exist in another language, this CSV file can be use to get a list of verses common to all languages.

## Paper Experiments

The speech-to-speech retrieval baseline model proposed at the paper is available [here](https://github.com/getalp/BibleNet).

## Citation

If you use this corpus in your experiments, please use the following bibtex for citation

@inproceedings{boito2020mass,
    title={MaSS: A Large and Clean Multilingual Corpus of Sentence-aligned Spoken Utterances Extracted from the Bible},
    author={Marcely Zanon Boito and William N. Havard and Mahault Garnerin and Éric Le Ferrand and Laurent Besacier},
    booktitle = {Language Resources and Evaluation Conference (LREC) 2020},
   year={2020},
 }
 
## Team and Contact

The people behind the (325) project:

* ![ORCiD Logo](https://zenodo.org/static/img/orcid.png) [Marcely ZANON BOITO](https://orcid.org/0000-0003-0134-6719)
* ![ORCiD Logo](https://zenodo.org/static/img/orcid.png) [William N. HAVARD](https://orcid.org/0000-0002-1226-4156)
* Mahault GARNERIN
* Eric Le FERRAND
* ![ORCiD Logo](https://zenodo.org/static/img/orcid.png) [Laurent BESACIER](https://orcid.org/0000-0001-7411-9125)

You can contact them at first.last-name@univ-grenoble-alpes.fr
