import json
import os
import numpy as np

collections = {'core18': {'input': '/home/breuert/data/orig/core18/',
                          'collection': 'WashingtonPostCollection',
                          'generator': 'WashingtonPostGenerator',
                          'threads': '1',
                          'topics': './anserini/src/main/resources/topics-and-qrels/topics.core18.txt'},
               'core17': {'input': '/home/breuert/data/orig/nyt_corpus/data/',
                          'collection': 'NewYorkTimesCollection',
                          'generator': 'DefaultLuceneDocumentGenerator',
                          'threads': '6',
                          'topics': './anserini/src/main/resources/topics-and-qrels/topics.core17.txt'},
               'robust04': {'input': '/home/breuert/data/orig/robust04/',
                            'collection': 'TrecCollection',
                            'generator': 'DefaultLuceneDocumentGenerator',
                            'threads': '6',
                            'topics': './anserini/src/main/resources/topics-and-qrels/topics.robust04.txt'},
               'robust05': {'input': '/home/breuert/data/orig/aquaint/',
                            'collection': 'TrecCollection',
                            'generator': 'DefaultLuceneDocumentGenerator',
                            'threads': '6',
                            'topics': './anserini/src/main/resources/topics-and-qrels/topics.robust05.txt'}}

stopwords = {'indri': './stopwords/en/indri.txt',
             'terrier': './stopwords/en/terrier.txt',
             'smart': './stopwords/en/smart.txt',
             'none': './stopwords/en/_none.txt'}

stemmers = ('porter', 'krovetz', 'none')

topicfields = ('title', 'title+description')


def cmd(search_config, keepStopwords=False, rm3=False):

    if keepStopwords and rm3:
        out = 'run.bm25+rm3.keepStopwords'
    if keepStopwords and not rm3:
        out = 'run.bm25.keepStopwords'
    if not keepStopwords and rm3:
        out = 'run.bm25+rm3.noStopwords'
    if not keepStopwords and not rm3:
        out = 'run.bm25.noStopwords'

    output_name = '.'.join([out,
                            search_config.get('stemmer'),
                            search_config.get('topicfield'),
                            search_config.get('index')])

    output = os.path.join('./anserini/runs/', output_name)

    cmd = ['./anserini/target/appassembler/bin/SearchCollection',
           '-index', os.path.join('./anserini/indexes/', search_config.get('index')),
           '-topicreader', 'Trec',
           '-topics', search_config.get('topics'),
           '-output', output,
           '-bm25',
           '-bm25.b', ' '.join(str(round(x, 3)) for x in np.arange(0.0, 1.05, 0.05)),
           '-bm25.k1', ' '.join(str(round(x, 3)) for x in np.arange(1.0, 2.05, 0.05)),
           '-stemmer', search_config.get('stemmer'),
           '-topicfield', search_config.get('topicfield'),
           '-runtag', 'ipm-repro']

    if keepStopwords:
        cmd.append('-keepStopwords')
    if rm3:
        cmd.extend(['-rm3',
                    '-rm3.fbTerms', ' '.join(str(x) for x in range(1, 11)),
                    '-rm3.fbDocs', ' '.join(str(x) for x in range(1, 11)),
                    '-rm3.originalQueryWeight', ' '.join(str(round(x, 3)) for x in np.arange(0.1, 1.0, 0.1))])

    return output_name, cmd


def index_config():
    out = {}
    for collection, properties in collections.items():
        for sw, sw_path in stopwords.items():
            for stemmer in stemmers:
                index_name = '.'.join([collection, sw, stemmer])
                index_config = {'collection': properties.get('collection'),
                                'input': properties.get('input'),
                                'index_name': index_name,
                                'generator': properties.get('generator'),
                                'threads': properties.get('threads'),
                                'stopwords': sw_path,
                                'stemmer': stemmer}
                out[index_name] = index_config

    with open('index.config', 'w') as f_out:
        f_out.write(json.dumps(out, indent=4))


def search_config():
    out = {}
    for collection, properties in collections.items():
        for sw, sw_path in stopwords.items():
            for stemmer in stemmers:
                for tf in topicfields:
                    index_name = '.'.join([collection, sw, stemmer])
                    search_config = {'index': index_name,
                                     'topics': properties.get('topics'),
                                     'stemmer': stemmer,
                                     'topicfield': tf}

                    search_name, search_cmd = cmd(search_config, keepStopwords=False, rm3=False)
                    out[search_name] = search_cmd
                    search_name, search_cmd = cmd(search_config, keepStopwords=True, rm3=False)
                    out[search_name] = search_cmd
                    search_name, search_cmd = cmd(search_config, keepStopwords=True, rm3=True)
                    out[search_name] = search_cmd
                    search_name, search_cmd = cmd(search_config, keepStopwords=False, rm3=True)
                    out[search_name] = search_cmd

    with open('search.config', 'w') as f_out:
        f_out.write(json.dumps(out, indent=4))


def main():
    index_config()
    search_config()


if __name__ == '__main__':
    main()

