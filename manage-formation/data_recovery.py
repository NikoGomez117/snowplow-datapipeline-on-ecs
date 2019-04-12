import sys
import boto3
import os
from datetime import datetime
from datetime import timedelta

def add_emr_steps(container_path,region,accessKey,secretKey,prodEnv,emrCluster,start_str,end_str):

	start = datetime.strptime(start_str, "%Y-%m-%d")
	end = datetime.strptime(end_str, "%Y-%m-%d")

	while start < end:

		# Actuall data flow runner command
		copy_load_delete_cmd = ("sudo " + 
		container_path +
		"/rs-loader-turbo_dir/files/dataflow-runner_dir/dataflow-runner" + " " +
		"run --emr-playbook" + " " +
		container_path +
		"/rs-loader-turbo_dir/files/dataflow-runner_dir/templates/rs-load-recovery" + " " +
		"--emr-cluster" + " " +
		emrCluster + " " +
		"--vars" + " " +
		"region," + region + "," +
		"accessKey," + accessKey + "," +
		"secretKey," + secretKey + "," +
		"prodEnv," + prodEnv + "," +
		"emrCluster," + emrCluster + "," +
		"pattern," + start.strftime("%Y-%m-%d") + "," +
		"timeStamp," + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
		
		os.system(copy_load_delete_cmd)

		start = start + timedelta(days=1)

if __name__ == "__main__":
    add_emr_steps(*sys.argv[1:])