import cv2
import csv
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from select_points import select_points
from warp_image import warp_image

def drawBox(image, boundary):
    x, y, w, h = int(boundary[0]), int(boundary[1]), int(boundary[2]), int(boundary[3])
    cv2.rectangle(image, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(image, "Tracking...", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

tracker = cv2.TrackerMOSSE_create()
# tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerMedianFlow_create()

camera = PiCamera() #  initialize the camera and grab a reference to the raw camera capture
camera.resolution = (1280,720)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(1280,720))
time.sleep(0.1) # allows the camera to warmup

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
rawCapture.truncate(0)

#_, img = cap.read()  # get initial image

coords, warped_img = select_points(image)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
rawCapture.truncate(0)
image = warp_image(image,coords)

bbox = cv2.selectROI("Tracking", image, False)  # select bounding box
tracker.init(image, bbox)  # initialize the tracker on the selected bounding box
#ok, img = cap.read()  # get the next image

#img = warp_image(img, coords) ## maybe i'll use this

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video = cv2.VideoWriter('Resources/geno_detect.mp4', fourcc, 30, (1080, 1920))


with open('location.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time","x_pixel", "y_pixel",])


for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port=True):
    timer = cv2.getTickCount()  # this is for the fps counter

    image = frame.array
    img = warp_image(image,coords)
    ok, bbox = tracker.update(img)  # updates with a new bounding box in the next frame

    if ok:
        drawBox(img, bbox)  # if the object is found, draw the new box on the image


        t = time.localtime()
        current_time = time.strftime("%Y/%m/%d %H:%M:%S", t)
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        x_pos = x + w / 2
        y_pos = y + h / 2

        with open('location.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, x_pos, y_pos])
            
        #time.sleep(3)
        
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)


    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)  # fps junk

    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Tracking", img)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

    #video.write(img)
    #ok, img = cap.read()  # get the next image in the stream for tracking
    #if ok:
    #    img = warp_image(img, coords)

cv2.destroyAllWindows()
# video.release()
