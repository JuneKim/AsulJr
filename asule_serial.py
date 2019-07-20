from serial import threaded

KEY_LEFT = 0
KEY_UP = 1
KEY_RIGHT = 2
KEY_DOWN = 3
KEY_SELECT = 4
KEY_START = 5
KEY_SQUARE = 6
KEY_TRIANGLE = 7
KEY_X = 8
KEY_CIRCLE = 9

Keymap = {
	b'a': [KEY_LEFT, 'KEY_LEFT'],
	b'w': [KEY_UP, 'KEY_UP'],
	b'd': [KEY_RIGHT, 'KEY_RIGHT'],
	b's': [KEY_DOWN, 'KEY_DOWN'],
	b'1': [KEY_SELECT, 'KEY_SELECT'],
	b'2': [KEY_START, 'KEY_START'],
	b'y': [KEY_SQUARE, 'KEY_SQUARE'],
	b'u': [KEY_TRIANGLE, 'KEY_TRIANGLE'],
	b'h': [KEY_X, 'KEY_X'],
	b'j': [KEY_CIRCLE, 'KEY_CIRCLE'],
}

class AsuleProtocol(threaded.Protocol):
	running = False
	def connection_mode(self, transport):
		self.transport = transport
		AsuleProtocol.running = True

	def connection_lost(self, exc):
		self.transport = None

	def data_received(self, data):
		return
	def write(self, data):
		print(data)
		self.transport.write(data)

	def isDone(self):
		return AsuleProtocol.running
