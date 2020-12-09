import logging
import subprocess
import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-11-openjdk-amd64'

cmd = ['./anserini/target/appassembler/bin/IndexCollection',
       '-collection', 'WashingtonPostCollection',
       '-input', '/home/breuert/data/orig/core18/',
       '-index', './anserini/indexes/lucene-index.core18',
       '-generator', 'WashingtonPostGenerator',
       '-threads', '1',
       '-storePositions',
       '-storeDocvectors',
       '-storeRaw',
       '-stopwords', '/home/breuert/code/stopwords/en/terrier.txt']


name = 'index-logger'
file = 'index.core18.log'
loglevel = logging.NOTSET
logging.basicConfig(level=loglevel,
                    filename=file,
                    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s - %(message)s')
logger = logging.getLogger(name)
logger.info("Logging started!")

subprocess.run(cmd)