import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from warp_image import warp_image

camera = PiCamera() #  initialize the camera and grab a reference to the raw camera capture
camera.resolution = (1280,720)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(1280,720))
time.sleep(0.1) # allows the camera to warmup

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
rawCapture.truncate(0)

coords = [[55, 326], [805, 277], [48, 636], [831, 559]]
image1 = warp_image(image,coords)

cv2.imwrite('cage.png',image1) 