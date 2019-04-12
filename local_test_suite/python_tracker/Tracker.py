from snowplow_tracker import *
from enum import Enum, unique
import time

class EnvironmentNotFoundException(Exception):
	pass

@unique
class Enviornment(Enum):
	LOCAL = 0
	DEV = 1
	PROD = 2

class SnowplowEnvironment(object):

	_url_map = {
		Enviornment.LOCAL: 'localhost:8030',
		Enviornment.DEV: 'localhost:8030',
		Enviornment.PROD: 'YOUR_PROD_ENDPOINT'
	}

	def __init__(self, env, _subject, _namespace, app_id):
		self.url = self._url(env)
		self.protocol = self._protocol(env)
		self.namespace = _namespace
		self.appId = app_id
		self.subject = _subject
		self.useBase64Encoding = self._use_base_64_encoding(env)

	def _url(self, env):
		try:
			return self._url_map[env]
		except KeyError:
			raise EnvironmentNotFoundException()

	def _protocol(self, env):
		return 'http' if env.value == Enviornment.PROD else 'http'

	def _use_base_64_encoding(self, env):
		return True if env.value == Enviornment.PROD else False

class AnalyticsTracker(object):

	def __init__(self, environment):
		self.e = Emitter(environment.url, environment.protocol)
		self.t = Tracker(self.e,
						 subject=environment.subject,
						 namespace=environment.namespace,
						 app_id=environment.appId,
						 encode_base64=environment.useBase64Encoding)


	def track(self, category, action, label=None, _property=None, value=None, context=None):
		self.t.track_struct_event(category, action, label, _property, value)

	def track_unstruct(self, json):
		self.t.track_self_describing_event(json)
