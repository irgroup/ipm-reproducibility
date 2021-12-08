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

**8. Retrieval**
```
python search.py
```
