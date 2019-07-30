# MaSS - Multilingual corpus of Sentence-aligned Spoken utterances

This is the repository for the CMU multilingual speech extension data set presented on the paper entitled *A Large and Clean Multilingual Corpus of Sentence Aligned Spoken Utterances Extracted from the Bible*.

## Data
For copyright reasons, we are not allowed to share the audio files however, we provide the extraction pipeline below. We also highlight this pipeline can be used to new languages of interested.
Inside the dataset folder, for each language we provide:
- Alignment textgrids (from Maus forced aligner)
- Final textual output
- [Mel Filterbank Spectrograms (such as used in the paper's experiments)](https://zenodo.org/record/3354711) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3354711.svg)](https://doi.org/10.5281/zenodo.3354711)


## Pipeline

### 1) Downloading audio chapters from [bible.is](bible.is).

  1.1. The audios used in our work are available in the following links:
  - [Basque data set](https://www.faithcomesbyhearing.com/audio-bibles/download/eus/EUSEABN1DA)
  - [English data set](https://www.faithcomesbyhearing.com/audio-bibles/download/eng/ENGESVN1DA)
  - [Finnish data set](https://www.faithcomesbyhearing.com/audio-bibles/download/fin/FIN38VN1DA)
  - [French data set](https://www.faithcomesbyhearing.com/audio-bibles/download/frn/FRNTLSN2DA)
  - [Hungarian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/hun/HUNHBSN1DA)
  - [Romanian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/ron/RONDCVN1DA)
  - [Russian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/rus/RUSS76N2DA)
  - [Spanish data set](https://www.faithcomesbyhearing.com/audio-bibles/download/spn/SPNBDAN1DA)

  1.2. The audios were converted from multi to single channel and forced aligned by using [this](https://github.com/getalp/multilingual-speech2speech-dataset/blob/master/scripts/force-align.py) script. 


### 2) Aligning the data with [Maus forced aligner](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSBasic)
For the covered languages, we make available the output from the Maus forced aligner in LANGUAGE/textgrid/. For new languages, please check the Website.

### 3) Obtaining speech alignment on a verse level
For each language, the audios were sliced in verses considering the output of 1.3. and the generated texgrids (2.). More details available [here](https://github.com/getalp/multilingual-speech2speech-dataset/blob/master/scripts/alignment/).

### 4) ID equivalence across languages
For translating the IDs in English, we provide the simple python script below.
~~~~
python3 scripts/fetch_data.py <language folder> <output folder> <language code>
~~~~

## Paper Experiments

The speech-to-speech retrieval baseline model proposed at the paper is available [here](https://github.com/getalp/BibleNet).

## Team and Contact

The people behind the (325) project:

* Marcely ZANON BOITO
* William N. HAVARD
* Mahault GARNERIN
* Eric Le FERRAND
* Laurent BESACIER

You can contact them at first.last-name@univ-grenoble-alpes.fr
