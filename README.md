# Setup instructions

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