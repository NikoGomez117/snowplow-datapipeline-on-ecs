FROM ubuntu:18.04

RUN apt-get update --fix-missing
RUN apt-get install default-jdk -y

ADD files/ $HOME

EXPOSE 80

CMD java -Xmx2G -jar snowplow-elasticsearch-loader-http-0.10.2.jar --config elastic-search-loader.conf
