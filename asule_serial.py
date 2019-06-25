
from serial import threaded

# 키 인덱스
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

class asuleProtocol(threaded.Protocol):
	def connection_mode(self, transport):
		self.transport = transport
		self.running = True

	def connection_lost(self, exc):
		self.transport = None

	def data_received(self, data):
		''' Todo '''
		if data in Keymap:
			print(Keymap[data][1])

			# Keymap[data][0]은 키 인덱스
            
			# 매칭되는 key 인덱스 가져옴
            key = Keymap[data][0]
            
            # 매핑 키가 CIRCLE 키이면 프로그램 종료        
            if key == KEY_CIRCLE:
                self.running = False
        else:
            print('Unknown data', data)

    # 데이터 보낼 때 함수
    def write(self,data):
        print(data)
        self.transport.write(data)
        
    # 종료 체크
    def isDone(self):
        return self.running