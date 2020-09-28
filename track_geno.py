import cv2
import csv
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from select_points import select_points
from warp_image import warp_image

time.sleep(30)

def drawBox(image, boundary):
    x, y, w, h = int(boundary[0]), int(boundary[1]), int(boundary[2]), int(boundary[3])
    cv2.rectangle(image, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(image, "Tracking...", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

#tracker = cv2.TrackerMOSSE_create()
# tracker = cv2.TrackerCSRT_create()
#tracker = cv2.TrackerMedianFlow_create()

camera = PiCamera() #  initialize the camera and grab a reference to the raw camera capture
camera.resolution = (1280,720)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(1280,720))
time.sleep(0.1) # allows the camera to warmup

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
rawCapture.truncate(0)

#_, img = cap.read()  # get initial image

#coords, image1 = select_points(image)
coords = [[55, 326], [805, 277], [48, 636], [831, 559]] # these two lines are for when you know the coordinates
image1 = warp_image(image,coords) # I want to run this automatically at boot without human intervention

#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
#rawCapture.truncate(0)
#image2 = warp_image(image,coords)

#bbox = cv2.selectROI("Tracking", image, False)  # select bounding box
#tracker.init(image, bbox)  # initialize the tracker on the selected bounding box
#ok, img = cap.read()  # get the next image

#img = warp_image(img, coords) ## maybe i'll use this

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video = cv2.VideoWriter('Resources/geno_detect.mp4', fourcc, 30, (1080, 1920))

t = time.localtime()
current_date = time.strftime("%Y%m%d", t)
csv_file = 'logged_data/' + current_date + '_location.csv'

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time","x_pixel", "y_pixel",])
    
x_pixel = np.zeros(5)
y_pixel = np.zeros(5)
counter = 0

for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port=True):
    timer = cv2.getTickCount()  # this is for the fps counter

    img = frame.array
    image2 = warp_image(img,coords)
    
    diff = cv2.absdiff(image1,image2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur= cv2.GaussianBlur(gray, (5,5),0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None,iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    largest = 0
    largest_contour = None
    
    for contour in contours:
        #(x,y,w,h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > largest:
            largest = cv2.contourArea(contour)
            largest_contour = contour
    if largest_contour is not None:

        (x,y,w,h) = cv2.boundingRect(largest_contour)
        cv2.rectangle(image1,(x,y),(x+w,y+h),(0,255,0),2)
        

        #x, y, w, h = int(contours[0]), int(contours[1]), int(contours[2]), int(contours[3])
        x_pos = x + w / 2
        y_pos = y + h / 2
        
        if counter < 4:
            x_pixel[counter] = x_pos
            y_pixel[counter] = y_pos
            counter += 1
            
        else:
            
            x_pixel[counter] = x_pos
            y_pixel[counter] = y_pos
            
            t = time.localtime()
            current_time = time.strftime("%Y/%m/%d %H:%M:%S", t)
            
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_time, np.average(x_pixel), np.average(y_pixel)])
                
            x_pixel = np.zeros(5)
            y_pixel = np.zeros(5)
            counter = 0
    #cv2.drawContours(image1, contours, -1, (0,255,0),2)
    
    #ok, new_bbox = tracker.update(img)  # updates with a new bounding box in the next frame

#    if contours:
#        
#        print(contours)
#        #drawBox(img, new_bbox)  # if the object is found, draw the new box on the image
#
#


        
#    else:
#        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)  # fps junk

    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    #cv2.imshow("Motion Detection", image1)
    #cv2.imshow("diff",diff)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
        
    image1 = image2

    #video.write(img)
    #ok, img = cap.read()  # get the next image in the stream for tracking
    #if ok:
    #    img = warp_image(img, coords)

cv2.destroyAllWindows()
# video.release()
