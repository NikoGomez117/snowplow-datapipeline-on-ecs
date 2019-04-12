FROM ubuntu:18.04

RUN apt-get update --fix-missing
RUN apt-get install default-jdk -y && apt-get install golang-go -y
RUN apt-get update && apt-get install vim -y

ADD files/ $HOME/root

EXPOSE 80

CMD /root/dataflow-runner_dir/dataflow-runner run --emr-playbook /root/dataflow-runner_dir/templates/rs-load --emr-cluster $EMR_ID --vars epochTime,1540322909
