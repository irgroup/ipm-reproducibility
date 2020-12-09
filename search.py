import logging
import subprocess
import os
import json


def main():
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-11-openjdk-amd64'
    log_path = './log'
    search_config_path = 'search.config'

    try:
        os.mkdir(log_path)
    except OSError as error:
        print(error)

    with open(search_config_path) as f_in:
        search_configs = json.loads(f_in.read())

    for run_name, cmd in search_configs.items():

        logging.basicConfig(level=logging.NOTSET,
                            filename=os.path.join(log_path, run_name),
                            format='%(asctime)s %(levelname)s %(filename)s %(funcName)s - %(message)s')
        logger = logging.getLogger('idx-log')

        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, ) as popen:
            for stdout_line in iter(popen.stdout.readline, b""):
                logger.info(stdout_line.strip())


if __name__ == '__main__':
    main()
