import unittest2

import logging
import inspect
import os
import sys
import inspect
import psutil
import sys, time
import pexpect
import time

from snowplow_tracker import Subject

from tests.mock_pipeline.mock_classes import MockIgluRepo, MockCollector, MockEnricher, MockS3
from tests.mock_pipeline.data_stream import Stream, Bucket
from python_tracker.Tracker import Enviornment, SnowplowEnvironment, \
	AnalyticsTracker

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TestAnalyticsTracker(AnalyticsTracker):
	pass


class RunnerUtility(object):
	__metaclass__ = Singleton

	# Mock classes
	m_iglu = MockIgluRepo()
	m_col = MockCollector()
	m_enrc = MockEnricher()
	m_s3 = MockS3()

	# Mock data stores
	stream_col_2_enrc = Stream(m_col,m_enrc)
	stream_enrc_2_s3 = Stream(m_enrc, m_s3)
	bucket_for_s3 = Bucket(m_s3)

	live_mocks = [stream_enrc_2_s3, stream_col_2_enrc, bucket_for_s3]

	is_initialized = False
	tracker = None

	def __init__(self):
		pass

	def log(self, output):
		print output

	def reset_mocks(self):
		for mock in self.live_mocks:
			mock.clear()

	def find_procs_by_name(self, name):
	    "Return a list of processes matching 'name'."
	    assert name, name
	    ls = []
	    for p in psutil.process_iter():
	        name_, exe, cmdline = "", "", []
	        try:
	            name_ = p.name()
	            cmdline = p.cmdline()
	            exe = p.exe()
	        except (psutil.AccessDenied, psutil.ZombieProcess):
	            pass
	        except psutil.NoSuchProcess:
	            continue

	        if name == name_ or cmdline[0] == name or os.path.basename(exe) == name:
	            ls.append(name)
	    return ls

	def setUp(self):
		is_initialized = True
		print "Starting Mocks and Processes"
		self.start_mocks()
		subject = Subject()
		subject.set_platform('pc')
		subject.set_user_id('123456')

		self.env = SnowplowEnvironment(Enviornment.LOCAL,
			subject,
			'testNameSpace',
			'testApp')

		self.tracker = TestAnalyticsTracker(self.env)
		self.tracker.util = self

	def tearDown(self):
		self.kill_mocks()

	def start_mocks(self):
		# starts up the first stream and waits for collector setup
		self.m_iglu.start()
		self.m_col.start(self.stream_col_2_enrc)
		self.m_enrc.start(self.stream_enrc_2_s3)
		self.m_s3.start(self.bucket_for_s3)
		self.m_col.blocking_setup()

	def exec_mocks(self):

		self.stream_col_2_enrc.clear()
		self.stream_enrc_2_s3.clear()
		self.bucket_for_s3.clear()

		self.stream_col_2_enrc.wait_for_message()
		self.stream_col_2_enrc.flush_serialized()
		self.stream_enrc_2_s3.wait_for_message(4)
		self.stream_enrc_2_s3.flush_raw()
		# print "Waiting For Data"
		# self.bucket_for_s3.wait_for_message(2)

	def kill_mocks(self):

		# cleanning up after execution
		self.m_col.shutdown()
		self.m_enrc.shutdown()
		self.m_s3.shutdown()
		self.stream_col_2_enrc.shutdown()
		self.stream_enrc_2_s3.shutdown()
		self.bucket_for_s3.shutdown()
		self.m_iglu.shutdown()


class TextTestRunner(unittest2.runner.TextTestRunner):

	def run(self, test, util):
		super(TextTestRunner, self).run(test)


util = RunnerUtility()

if __name__ == "__main__":
	if not util.is_initialized:
		print "Test Runner Setting up..."
		util.setUp()

		loader = unittest2.TestLoader()
		testsuites = loader.discover('.')
		testRunner = TextTestRunner()

		## So help me god....
		for suite in testsuites:
			for testcollection in suite._tests:
				for test in testcollection:
					test.util = util

		testRunner.run(testsuites, util)

		print "Test Runner Tearing Down..."
		util.tearDown()
