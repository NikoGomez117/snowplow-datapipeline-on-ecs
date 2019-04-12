FROM ubuntu:18.04

RUN apt-get update --fix-missing
RUN apt-get install default-jdk -y

ADD files/ $HOME

EXPOSE 80

CMD java -Xmx2G -jar snowplow-stream-enrich-kinesis-0.18.0.jar --config enricher.conf --resolver file:resolver.json --enrichments file:enrich_configs/
