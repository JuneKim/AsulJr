from asule_message import Message
from asule_detection import AsuleDetection

import numpy as np
import cv2
import os

class AsuleRedballDetection(AsuleDetection):

	def run(self):
		msg = Message()
		ret, frame = self._capture.read()
		if not ret:
			print ('error: fail to get image')
			return msg

		frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		''' may need to modify range '''
		threshLow = cv2.inRange(frameHSV, (0, 100, 100), (10, 255, 255))
		threshHigh = cv2.inRange(frameHSV, (160, 100, 100), (179, 255, 255))
		cv2.imshow('threshLow', threshLow)
		cv2.imshow('threshHigh', threshHigh)

		frameRed = cv2.addWeighted(threshLow, 1.0, threshHigh, 1.0, 0.0)
		frameRed = cv2.GaussianBlur(frameRed, (9, 9), 3, 3)


		frameRed = cv2.dilate(frameRed, np.ones((5, 5), np.uint8))
		frameRed = cv2.erode(frameRed, np.ones((5, 5), np.uint8))
		
		cv2.imshow('frameRed', frameRed)
		rows, cols = frameRed.shape

		circles = cv2.HoughCircles(frameRed, cv2.HOUGH_GRADIENT, 2, rows/4)
		idx = 0
		if circles is not None:
			for circle in circles[0]:
				''' circles found @ (x, y)'''
				idx += 1
				x, y, r = circle
				cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
				cv2.circle(frame, (x, y), r, (0, 0, 255), 3)

		return msg

	def stop(self):
		pass