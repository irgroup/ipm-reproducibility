```
#!/bin/bash

git submodule update --init --recursive
cd anserini/tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
mvn clean package appassembler:assemble -DskipTests -Dmaven.javadoc.skip=true
``` 