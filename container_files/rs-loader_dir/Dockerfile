FROM ubuntu:18.04

RUN apt-get update --fix-missing
RUN apt-get install default-jdk -y && apt-get install golang-go -y
# RUN apt-get update && apt-get -y install cron
RUN apt-get update && apt-get install vim -y

ADD files/ $HOME/root

EXPOSE 80

# RUN chmod 0644 ./root/dataflow-runner_dir/rs-load-cron
# RUN crontab ./root/dataflow-runner_dir/rs-load-cron
# RUN touch ./var/log/cron.log
# CMD bash /root/cron-env-conf.sh && tail -f /var/log/cron.log
CMD /root/dataflow-runner_dir/dataflow-runner run --emr-playbook /root/dataflow-runner_dir/templates/rs-load --emr-cluster $EMR_ID --vars timeStamp,$(date '+%Y-%m-%d-%H-%M-%S')
