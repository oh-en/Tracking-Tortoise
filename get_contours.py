import cv2
import numpy as np

img = cv2.imread("Resources/IMG_20200825_132435.jpg")
#img = cv2.imread("Resources/IMG_20200825_132443.jpg")
img = cv2.resize(img, (int(720 * 3 / 2), 720))

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 100, 100)
kernel = np.ones((5, 5))
imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
imgThre = cv2.erode(imgDial, kernel, iterations=2)

contours, hiearchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('Canny', imgThre)
cv2.waitKey(0)
