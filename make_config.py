import json

collections = {'core18': {'input': '/home/breuert/data/orig/core18/',
                          'collection': 'WashingtonPostCollection',
                          'generator': 'WashingtonPostGenerator',
                          'threads': '1'},
               'core17': {'input': '/home/breuert/data/orig/nyt_corpus/data/',
                          'collection': 'NewYorkTimesCollection',
                          'generator': 'DefaultLuceneDocumentGenerator',
                          'threads': '6'},
               'robust04': {'input': '/home/breuert/data/orig/robust04/',
                            'collection': 'TrecCollection',
                            'generator': 'DefaultLuceneDocumentGenerator',
                            'threads': '6'},
               'robust05': {'input': '/home/breuert/data/orig/aquaint/',
                            'collection': 'TrecCollection',
                            'generator': 'DefaultLuceneDocumentGenerator',
                            'threads': '6'}}

stopwords = {'indri': './stopwords/en/indri.txt',
             'terrier': './stopwords/en/terrier.txt',
             'smart': './stopwords/en/smart.txt',
             'none': './stopwords/en/_none.txt'}

stemmers = ('porter', 'krovetz', 'none')

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
