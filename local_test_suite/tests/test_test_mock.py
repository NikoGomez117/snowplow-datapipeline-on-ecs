import json
from snowplow_tracker import SelfDescribingJson
from test_base_test_case import BaseTestCase

class MockTestCase(BaseTestCase):

	def test_schemas(self):
		td = open("test_data",'r')
		while True:
			event_name = td.readline().rstrip('\n')
			schema = td.readline().rstrip('\n')
			payload = td.readline().rstrip('\n')
			if not payload: break
			self.util.tracker.track_unstruct(SelfDescribingJson(schema,json.loads(payload)))
			self.assertEventTracked(event_name)
		td.close()