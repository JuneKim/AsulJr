from asule_serial import AsuleProtocol
from asule_message import Message
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

g_tasks = queue.Queue()
DEBUG_ENABLED = True
 
def runTasks(p):
	if g_tasks.empty() == False:
		try:
			msg = g_tasks.get_nowait()
			p.write(msg.getStream())
		except:
			print ('Error:get_nowait')


def main():

	timerSec = 1
	# Run Camera / Img processing
	cam = AsuleCamera(g_tasks)
	#cam.setDaemon(True)
	logging.debug ('cam before')
	cam.start()
	logging.debug ('cam start')
	#if is_bt_on == True:
	#
	#else:
	try:
		ser = serial.serial_for_url(PORT, baudrate = 115200, timeout=1)
		logging.debug('1')
		with serial.threaded.ReaderThread(ser, AsuleProtocol) as p:
			logging.debug('2')
			#while p.isDone():
			while 1:
				logging.debug('isDone')
				# do something
				runTasks(p)
				if DEBUG_ENABLED:
					frame = cam.read()
					cv2.imshow('result', frame)
					if cv2.waitKey(1) == 27:
						break

			logging.debug('3')

	except serial.serialutil.SerialException:
		logging.error("fail to open serial port")

if __name__ == '__main__':
	main()
