# An in-depth Investigation on the Behaviour of Measures to Quantify Reproducibility

This repository contains the source code and scripts. The accompanying data and experimental outcomes can be found on [Zenodo](https://zenodo.org/record/5902542).

## Abstract
> Science is now facing a so-called reproducibility crisis, i.e., when researchers repeat an experiment they struggle to get the same or comparable results. This represents a fundamental problem in any scientific discipline because reproducibility lies at the very basis of the scientific method. This paper focuses on measures to quantify reproducibility in IR and their behavior. Current reproducibility practices rely mainly on the comparison of averaged scores: if the reproduced score is close enough to the original one, the reproducibility experiment is deemed successful. We generate reproducibility runs in a controlled experimental setting, which allows us to control the amount of reproducibility error. We investigate the behaviour of different reproducibility measures with these synthetic runs in 3 different scenarios. Experimental results show that a single score is not enough to decide whether an experiment is successfully reproduced because such score depends on the type of effectiveness measure and the performance of the original run. This highlights how challenging it can be not only to reproduce experimental results but also to quantify the amount of reproducibility.

## Instructions to reproduce the setup and experiments

1. Clone this repository:
```
git clone --recurse-submodules https://github.com/irgroup/ipm-reproducibility.git
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

9. Simulate runs: `python scripts/simulate_run.py`

10. Run the Juypter notebooks in `notebooks/` to perform swaps and replacements and make the heatmaps. 
