import pexpect
import re

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

import base64

def SerializeThriftMsg(msg, protocol_type=TBinaryProtocol.TBinaryProtocol):
    """Serialize a thrift message using the given protocol.

    The default protocol is binary.

    Args:
        msg: the Thrift object to serialize.
        protocol_type: the Thrift protocol class to use.

    Returns:
        A string of the serialized object.
    """
    msg.validate()
    transportOut = TTransport.TMemoryBuffer()
    protocolOut = protocol_type(transportOut)
    msg.write(protocolOut)
    return transportOut.getvalue()


def DeserializeThriftMsg(msg, data,
                         protocol_type=TBinaryProtocol.TBinaryProtocol):
    """Deserialize a thrift message using the given protocol.

    The default protocol is binary.

    Args:
        msg: the Thrift object to serialize.
        data: the data to read from.
        protocol_type: the Thrift protocol class to use.

    Returns:
        Message object passed in (post-parsing).
    """
    transportIn = TTransport.TMemoryBuffer(data)
    protocolIn = protocol_type(transportIn)
    msg.read(protocolIn)
    msg.validate()
    return msg

def ExpectedNotFound(Exception):
	pass

class DataStore:
    lines_processed = []

    def get_sink(self):
        return self.sink

    def wait_for_message(self, line_total=1, condition=['.+\r\n']):
        try:
            for num in range(line_total):
                i = self.source._process.expect(condition, timeout=4)
        except pexpect.TIMEOUT:
            print "Pexpect TIMEOUT"

    def shutdown(self):
        self.sink.close()

    def clear(self):
    	self.reset()
        self.sink.seek(0)
        self.sink.truncate()

    def reset(self):
		self.lines_processed = []

class Stream(DataStore):

    _close_stream_error = 'Error deserializing raw event: Cannot read. Remote side has closed. Tried to read 1 bytes, but only got 0 bytes'

    def __init__(self,src,tar):
        self.source = src
        self.target = tar
        self.sink = open("./mock_streams/{}_to_{}".format(src.get_name(),tar.get_name()),'w+')

    def flush_raw(self):
        self.sink.seek(0)
        for line in self.sink:
            if self._close_stream_error in line:
                pass
            else:
                self.lines_processed.append(line)

    def flush_serialized(self):
        self.sink.seek(0)
        pattern = re.compile('.+\r\n')
        for line in self.sink:
            if self._close_stream_error in line:
                pass
            elif pattern.match(line):
                self.lines_processed.append(base64.b64decode(line))
                self.target._process.sendline(line)

class Bucket(DataStore):

	def __init__(self,src):
		self.source = src
		self.sink = open("./mock_streams/{}_bucket".format(src.get_name()),'w+')
