from asule_protocol import AsuleProtocol
from asule_message import AsuleMessage
from asule_camera import AsuleCamera

import logging
import sys
if sys.version_info[0] == 2:
	import Queue as queue
else:
	import queue as queue

import serial
import time
import cv2


# global setting
PORT = '/dev/ttyACM0'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(threadName)s [%(funcName)s:%(lineno)d] %(levelname)s %(message)s')

g_inqueue = queue.Queue()
g_outqueue = queue.Queue()
DEBUG_ENABLED = True
MAJOR_VERSION = 1
MINOR_VERSION = 1
 
def runTasks(p):
	if g_inqueue.empty() == False:
		msg = g_inqueue.get_nowait()
		if msg is None:
			logging.debug(msg)

	if g_outqueue.empty() == False:
		msg = g_outqueue.get_nowait()
		if msg is not None:
			logging.debug(msg)
			#p.write(msg)

def main():
	logging.debug("AsuleJr v{}.{} is running.".format(MAJOR_VERSION, MINOR_VERSION))
	timerSec = 1
	# Run Camera / Img processing
	cam = AsuleCamera(g_outqueue)
	#cam.setDaemon(True)
	cam.start()
	logging.debug ('cam start')
	#if is_bt_on == True:
	#
	#else:
	try:
		ser = serial.serial_for_url(PORT, baudrate = 115200, timeout=1)
		with serial.threaded.ReaderThread(ser, AsuleProtocol) as p:
			p.setQueue(g_inqueue)
			#while p.isDone():
			while 1:
				# do something
				runTasks(p)
				if DEBUG_ENABLED:
					frame = cam.read()
					cv2.imshow('result', frame)
					if cv2.waitKey(1) == 27:
						break

	except serial.serialutil.SerialException:
		logging.error("fail to open serial port")

if __name__ == '__main__':
	main()
