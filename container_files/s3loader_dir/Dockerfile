FROM ubuntu:18.04

RUN apt-get update --fix-missing
RUN apt-get install default-jdk -y

RUN apt-get update
RUN apt-get install lzop liblzo2-dev -y

ADD files/ $HOME

EXPOSE 80

CMD java -Xmx2G -jar snowplow-s3-loader-0.6.0.jar --config s3loader.conf
