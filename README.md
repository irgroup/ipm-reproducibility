## Instructions to reproduce the setup and experiments

1. Clone this repository:
```
git clone --recurse-submodules https://github.com/irgroup/ipm-repro.git
```

2. Build anserini and the corresponding tools: `sh build.sh`

3. Install requirements: `pip install -r requirements.txt`

4. Specify the paths to the input data in `make_config.py`, e.g. for the TREC Washington Post Collection:
```
'core18': {'input': '/SPECIFY/YOUR/PATH/HERE',
           'collection': 'WashingtonPostCollection',        
           'generator': 'WashingtonPostGenerator',
           'threads': '1'}
```

5. Specifiy the path to your Java 11 installation and add it with `os.environ['JAVA_HOME']` in `make_index.py` and `search.py`.

6. Make the `index.config` and `search.config` files with: `python scripts/make_config.py`

7. Build indexes with `make_index.py`: `python scripts/make_index.py`

8. Retrieval of real runs: `python scripts/search.py`
