import logging
import subprocess
import os
import json


def cmd(index_name, index_config):
    return ['./anserini/target/appassembler/bin/IndexCollection',
            '-collection', index_config.get('collection'),
            '-input', index_config.get('input'),
            '-index', os.path.join('./anserini/indexes/', index_name),
            '-generator', index_config.get('generator'),
            '-threads', index_config.get('threads'),
            '-storePositions',
            '-storeDocvectors',
            '-storeRaw',
            '-storeContents',
            '-stopwords', index_config.get('stopwords'),
            '-stemmer', index_config.get('stemmer')]


def main():
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-11-openjdk-amd64'
    log_path = './log'
    idx_config_path = 'index.config'

    try:
        os.mkdir(log_path)
    except OSError as error:
        print(error)

    idx_configs = {}
    with open(idx_config_path) as f_in:
        idx_configs = json.loads(f_in.read())

    for idx_name, idx_config in idx_configs.items():
        idx_cmd = cmd(idx_name, idx_config)

        logging.basicConfig(level=logging.NOTSET,
                            filename=os.path.join(log_path, idx_name),
                            format='%(asctime)s %(levelname)s %(filename)s %(funcName)s - %(message)s')
        logger = logging.getLogger('idx-log')

        with subprocess.Popen(idx_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, ) as popen:
            for stdout_line in iter(popen.stdout.readline, ""):
                logger.info(stdout_line.strip())


if __name__ == '__main__':
    main()
