# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch:5.5.2

RUN bin/elasticsearch-plugin install http://dl.bintray.com/content/imotov/elasticsearch-plugins/org/elasticsearch/elasticsearch-analysis-morphology/5.5.2/elasticsearch-analysis-morphology-5.5.2.zip
RUN bin/elasticsearch-plugin install analysis-phonetic


USER root

COPY compose/elasticsearch/elasticsearch.yml  /usr/share/elasticsearch/config/elasticsearch.yml
RUN chown elasticsearch:elasticsearch /usr/share/elasticsearch/config/elasticsearch.yml


USER elasticsearch
