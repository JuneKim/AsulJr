from asule_detection import AsuleDetection

import numpy as np
import cv2
import os
import logging

class AsuleFaceDetection(AsuleDetection):

	def __init__(self, capture):
		super().__init__(capture)
		print (os.getcwd() + '/haarcascade_frontalface_default.xml')
		self.face_cascade = cv2.CascadeClassifier(os.getcwd() + '/haarcascade_frontalface_default.xml')
		#opencv-python/data/haarcascades/haarcascade_frontalface_default.xml


	def run(self):
		ret, frame = self._capture.read()
		if not ret:
			print ('error: fail to get image')
			return (0, 0, 0, 0, frame)
		frame = cv2.flip(frame, -1)
		frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


		faces = self.face_cascade.detectMultiScale(frameGray, 1.1, 4)

		x = y = w = h = 0.0
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
			logging.debug("face found")

		return (x, y, x + w, y + h, frame)

	def stop(self):
		pass
