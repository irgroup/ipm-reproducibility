## Datasets

| collection | docs | index time | index size | source | qrels | topics | 
| --- | --- | --- | --- | --- | --- | --- |
| core17 | 1.8 million | 00:07:03 | 8.4 GB | [New York Times Annotated Corpus](https://catalog.ldc.upenn.edu/LDC2008T19)| [Core17](https://trec.nist.gov/data/core/qrels.txt)| [Core17](https://trec.nist.gov/data/core/core_nist.txt)|
| core18 | 0.6 million | 00:09:17 | 4.8 GB |[TREC Washington Post Corpus](https://trec.nist.gov/data/wapost/) | [Core18](https://trec.nist.gov/data/core/qrels2018.txt)| [Core18](https://trec.nist.gov/data/core/topics2018.txt)|
| robust04 | 0.5 million | 00:01:28 | 2.0 GB | [TREC disks 4 and 5](https://trec.nist.gov/data/cd45/index.html)| [Robust04](https://trec.nist.gov/data/robust/qrels.robust2004.txt)| [Robust04](https://trec.nist.gov/data/robust/04.testset.gz)|
| robust05 | 1 million | 00:02:25 | 3.6 GB | [The AQUAINT Corpus of English News Text](https://catalog.ldc.upenn.edu/LDC2002T31)| [Robust05](https://trec.nist.gov/data/robust/05/TREC2005.qrels.txt)| [Robust05](https://trec.nist.gov/data/robust/05/05.50.topics.txt)|

## Setup instructions

**1. Clone this repository:**
```
git clone --recurse-submodules https://github.com/breuert/ipm-repro.git
```

**2. Build anserini and the corresponding tools:**
```
sh build.sh
```

alternatively run:
```
cd anserini/tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
mvn clean package appassembler:assemble -DskipTests -Dmaven.javadoc.skip=true
``` 

**3. Specify the paths to the input data in `make_config.py`, e.g. for the TREC Washington Post Collection:**
```
'core18': {'input': '/SPECIFY/YOUR/PATH/HERE',
           'collection': 'WashingtonPostCollection',        
           'generator': 'WashingtonPostGenerator',
           'threads': '1'}
```

**4. Make the `index.config` file with:**
```
python make_config.py
```

It will ouput a file with entries like this one:

    "robust04.indri.krovetz": {
        "collection": "TrecCollection",
        "input": "/home/breuert/data/orig/robust04/",
        "index_name": "robust04.indri.krovetz",
        "generator": "DefaultLuceneDocumentGenerator",
        "threads": "6",
        "stopwords": "./stopwords/en/indri.txt",
        "stemmer": "krovetz"
    }

**5. Build indexes with `make_index.py`**
```
python make_index.py
```