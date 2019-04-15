# Multilingual speech2speech dataset

This is the repository for the CMU multilingual speech extension data set presented on the paper entitled *A Large and Clean Multilingual Corpus of Sentence Aligned Spoken Utterances Extracted from the Bible*.

The data and scripts will be uploaded in the upcoming weeks.



## Pipeline

* 1) Downloading audio chapters from [bible.is](bible.is)
-> Getting the data
-> Going from multi to one channel

[English data set](https://www.faithcomesbyhearing.com/audio-bibles/download/eng/ENGESVN1DA)

[French data set](https://www.faithcomesbyhearing.com/audio-bibles/download/frn/FRNTLSN2DA)

[Spanish data set](https://www.faithcomesbyhearing.com/audio-bibles/download/spn/SPNBDAN1DA)

[Romanian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/ron/RONDCVN1DA)

[Basque data set](https://www.faithcomesbyhearing.com/audio-bibles/download/eus/EUSEABN1DA)

[Russian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/rus/RUSS76N2DA)

[Hungarian data set](https://www.faithcomesbyhearing.com/audio-bibles/download/hun/HUNHBSN1DA)

[Finnish data set](https://www.faithcomesbyhearing.com/audio-bibles/download/fin/FIN38VN1DA)


* 2) Aligning the data with [Maus forced aligner](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSBasic)

* 3) Obtaining speech alignment on a verse level

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
