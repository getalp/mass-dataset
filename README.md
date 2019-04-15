# Multilingual speech2speech dataset

This is the repository for the CMU multilingual speech extension data set presented on the paper entitled *A Large and Clean Multilingual Corpus of Sentence Aligned Spoken Utterances Extracted from the Bible*.

The data and scripts will be uploaded in the upcoming weeks.



## Pipeline

1) Downloading audio chapters from [bible.is](bible.is).
The audios used in our work are available in the following links:
  - [Basque data set](https://www.faithcomesbyhearing.com/audio-bibles/download/eus/EUSEABN1DA)
  - [English data set](https://www.faithcomesbyhearing.com/audio-bibles/download/eng/ENGESVN1DA)
  - [Finnish data set](https://www.faithcomesbyhearing.com/audio-bibles/download/fin/FIN38VN1DA)
  - [French data set](https://www.faithcomesbyhearing.com/audio-bibles/download/frn/FRNTLSN2DA)
  - [Hungarian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/hun/HUNHBSN1DA)
  - [Romanian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/ron/RONDCVN1DA)
  - [Russian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/rus/RUSS76N2DA)
  - [Spanish data set](https://www.faithcomesbyhearing.com/audio-bibles/download/spn/SPNBDAN1DA)

The audios were convered from multi to single channel by using [this]() script. And [this]() script was used to generated the input for the Maus forced aligner (verse information removal).

2) Aligning the data with [Maus forced aligner](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSBasic)
For the covered languages, we make available the output from the Maus forced aligner in LANGUAGE/textgrid/. For new languages, please check the Website.

3) Obtaining speech alignment on a verse level
For each languages, the audios were sliced in verses considering the raw chapter text and the generated texgrids. More details available [here](https://github.com/getalp/multilingual-speech2speech-dataset/blob/master/scripts/alignment/).

## Paper Experiments

The implementation and models presented in the paper are available [here](https://github.com/getalp/BibleNet).

## Team and Contact

The people behind the (325) project:

* Eric Le FERRARD
* William HAVARD
* Marcely ZANON BOITO
* Mahault GARNERIN
* Laurent BESACIER

You can contact them at first.last-name@univ-grenoble-alpes.fr
