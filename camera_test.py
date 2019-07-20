import cv2

capture = cv2.VideoCapture(-1)

capture.set(cv2.CAP_PROP_FPS, 60)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
while(capture.isOpened()):
	ret, frame = capture.read()
	if ret:
		frame = cv2.flip(frame, -1)
		gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		cv2.imshow('result', gray_img)
		k = cv2.waitKey(1) & 0xFF
		if (k == 27):
			break
capture.release()
cv2.destroyAllWindows()

