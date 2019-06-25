from asule_serial import asuleProtocol
from asule_message import Message
from asule_camera import runCamera

import sys
if sys.version[0] == '2':
	import Queue as queue # python 2.x
else:
	import queue as queue # python 3.x

import logging

# global setting
PORT = '/dev/ttyUSB0'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(thead)d,%(name)s %(levelname)s %(message)s')

g_tasks = Queue()

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
	cam = Thread(target = runCamera, args=(g_tasks,))
	#cam.setDaemon(True)
	cam.start()

	#if is_bt_on == True:
	#
	#else:
	ser = serial.serial_for_url(PORT, baudrate = 9600, timeout=1)
	with ReaderThread(ser, asuleProtocol) as p:
	while p.isDone():
		# do something
		runTasks(p)
		time.sleep(timerSec)

if __name__ == '__main__':
	main()