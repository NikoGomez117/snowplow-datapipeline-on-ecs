import pexpect
from data_stream import Stream, Bucket

# For Iglu Repo
import SimpleHTTPServer
import SocketServer
import requests
import multiprocessing
import os

class BaseMockClass:

	_name = 'base'
	_process = None

	def get_name(self):
		return self._name

	def shutdown(self):
		if self._process != None:
			self._process.close()
			self._process = None

class MockCollector(BaseMockClass):

	_name = 'collector'

	_dir = './collector/'
	_jar_name = 'snowplow-stream-collector-stdout-0.14.0.jar'
	_jar_path = "{}{}".format(_dir, _jar_name)
	_config_name = 'test.conf'
	_config_path = "{}{}".format(_dir, _config_name)
	_cmd = "java -jar {} --config {}".format(_jar_path,_config_path)

	def start(self, output_stream):
		if self._process == None:
			self._process = pexpect.spawn(self._cmd,timeout=600)
			self._process.logfile_read = output_stream.get_sink()

	def blocking_setup(self):
		self._process.expect(['8030\r\n'])


class MockEnricher(BaseMockClass):

	_name = 'enricher'

	_dir = './enricher/'
	_jar_name = 'snowplow-stream-enrich-stdin-0.18.0.jar'
	_jar_path = "{}{}".format(_dir, _jar_name)
	_config_name = 'test.conf'
	_config_path = "{}{}".format(_dir, _config_name)
	_resolver_name = 'resolver.json'
	_resolver_path = "{}{}".format(_dir, _resolver_name)
	_enrichments_name = 'enrich_configs/'
	_enrichments_path = "{}{}".format(_dir,_enrichments_name)
	_cmd = "java -jar {} --config {} --resolver file:{} --enrichments file:{}".format(_jar_path,_config_path,_resolver_path,_enrichments_path)

	def start(self, output_stream):
		if self._process == None:
			self._process = pexpect.spawn(self._cmd,timeout=600)
			self._process.logfile_read = output_stream.get_sink()

	# Does not need a blocking setup (just reads from the input restfully)

class MockS3(BaseMockClass):

	_name = "S3"

	def start(self, output_bucket):
		if self._process == None:
			self._process = pexpect.spawn('echo ''',timeout=600)
			self._process.logfile_read = output_bucket.get_sink()

class MockIgluRepo(BaseMockClass):

	_name = 'iglu-repo'

	PORT = 8020
	URL = 'localhost:{port}'.format(port=PORT)

	def start(self):
		if self._process == None:
			old_dir = os.getcwd()
			parent_dir = old_dir[:-16]
			os.chdir(parent_dir+"container_files/iglu-repo_dir/")
			Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
			httpd = SocketServer.TCPServer(("", self.PORT), Handler)
			print "serving Iglu Repo at port", self.PORT

			self._process = multiprocessing.Process(target=httpd.serve_forever)
			self._process.daemon = True
			self._process.start()
			os.chdir(old_dir)

	def shutdown(self):
		if self._process != None:
			self._process.terminate()
			self._process = None