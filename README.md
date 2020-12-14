## Current status

- [x] Principled generation of index and search configurations that can be used with [Anserini](https://github.com/castorini/anserini)
- [x] Generation of Lucene-based indexes with Anserini
- [x] Runs derived from Lucene-based indexes with Anserini
- [ ] Runs derived with other toolkits like [Terrier](https://github.com/terrier-org/terrier-core) or [Lucindri](https://github.com/lemurproject/Lucindri)

## Notes

- :heavy_check_mark: Directly ingesting the Lucene-based index with the [Lucene plugin](https://github.com/terrierteam/terrier-lucene) of [Terrier](https://github.com/terrier-org/terrier-core) without converting the index into the [CIFF](https://github.com/osirrc/ciff) format and deriving runs based on BM25
- :x: Could not ingest the Lucene-based index into [Lucindri](https://github.com/lemurproject/Lucindri) &rarr; discrepancy between Lucene versions
- :x: [Lucindri](https://github.com/lemurproject/Lucindri) does not support BM25+RM3 at the current stage
- :x: Could not run the [CIFF plugin of Terrier](https://github.com/terrierteam/terrier-ciff)
- :x: Could not run the [PRF plugin of Terrier](https://github.com/terrierteam/terrier-prf), that is required for RM3, in combination with the [Lucene plugin of Terrier](https://github.com/terrierteam/terrier-lucene)
- :x: The other retrieval toolkits supporting [CIFF](https://github.com/osirrc/ciff) do not implement any PRF mechanisms like RM3

### Links

- [Shared resources, e.g. runs](https://th-koeln.sciebo.de/s/cP1ddwW4LpTN8y6)

## Considered components and corresponding variations

### Indexing

- Collection = {Core17, Core18, Robust04, Robust05}
- Stopwords = {None, Indri, Terrier, SMART}
- Stemmers = {None, Porter, Krovetz}

**Under the consideration of all possible combinations, this will result in 48 indexes.**

### Retrieval

- Retrieval methods = {BM25, BM25+RM3}
- Considered topicfields for the query = {Title, Title+Description}
- Stopwords [y/n]
- Stemmers = {None, Porter, Krovetz}
- BM25.k1 = [1.0 ... 2.0]
- BM25.b = [0.0 ... 1.0]
- RM3's number of feedback terms = [1 ... 10]
- RM3's number of feedback documents = [1 ... 10]
- RM3's weighting of old query = [0.1 ... 0.9]

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
git clone --recurse-submodules https://github.com/irgroup/ipm-repro.git
```

**2. Build anserini and the corresponding tools:**
```
sh build.sh
```

**3. Install requirements**
```
pip install -r requirements.txt
```

**4. Specify the paths to the input data in `make_config.py`, e.g. for the TREC Washington Post Collection:**
```
'core18': {'input': '/SPECIFY/YOUR/PATH/HERE',
           'collection': 'WashingtonPostCollection',        
           'generator': 'WashingtonPostGenerator',
           'threads': '1'}
```

**5. Specifiy the path to your Java 11 installation and add it with `os.environ['JAVA_HOME']` in `make_index.py` and `search.py`.**

**6. Make the `index.config` and `search.config` files with:**
```
python make_config.py
```

`index.config` will contain entries like this one:

    "robust04.indri.krovetz": {
        "collection": "TrecCollection",
        "input": "/home/breuert/data/orig/robust04/",
        "index_name": "robust04.indri.krovetz",
        "generator": "DefaultLuceneDocumentGenerator",
        "threads": "6",
        "stopwords": "./stopwords/en/indri.txt",
        "stemmer": "krovetz"
    }

`search.config` will contain entries like this one:

    "run.bm25.noStopwords.porter.title.core18.indri.porter": [
        "./anserini/target/appassembler/bin/SearchCollection",
        "-index",
        "./anserini/indexes/core18.indri.porter",
        "-topicreader",
        "Trec",
        "-topics",
        "./anserini/src/main/resources/topics-and-qrels/topics.core18.txt",
        "-output",
        "./anserini/runs/run.bm25.noStopwords.porter.title.core18.indri.porter",
        "-bm25",
        "-bm25.b",
        "0.0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 1.0",
        "-bm25.k1",
        "1.0 1.05 1.1 1.15 1.2 1.25 1.3 1.35 1.4 1.45 1.5 1.55 1.6 1.65 1.7 1.75 1.8 1.85 1.9 1.95 2.0",
        "-stemmer",
        "porter",
        "-topicfield",
        "title",
        "-runtag",
        "ipm-repro"
    ]

**7. Build indexes with `make_index.py`**
```
python make_index.py
```

If you use all four test collections, this will results in 48 indexes with a total size of **225,6G** [1].

**8. Retrieval**
```
python search.py
```

---
[1]  12*(8.4G+4.8G+2.0G+3.6G)=225,6G