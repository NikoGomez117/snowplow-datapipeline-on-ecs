FROM ubuntu:18.04

RUN apt-get update --fix-missing
RUN apt-get install default-jdk -y

ADD files/ $HOME

EXPOSE 80

CMD java -Xmx2G -jar snowplow-stream-collector-kinesis-0.14.0.jar --config collector.conf
