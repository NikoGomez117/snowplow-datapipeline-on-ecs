import unittest2
from  __builtin__ import any as b_any

class BaseTestCase(unittest2.TestCase):

	def setUp(self):
		#self.util.reset_mocks()
		pass

	def assertEventTracked(self, actionString):
		print "mock execution"

		result = True
		try:
			self.util.exec_mocks()
			print "success"
		except Exception as e:
			result = False
			print type(e)

		self.assertTrue(result)
		self.assertTrue(b_any(actionString in x for x in self.util.stream_enrc_2_s3.lines_processed))#stream_col_2_enrc.lines_processed))
		self.assertFalse(b_any("\"errors\":" in x for x in self.util.stream_enrc_2_s3.lines_processed))

	def tearDown(self):
		#self.util.reset_mocks()
		pass