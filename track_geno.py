import cv2

def drawBox(image, boundary):
    x, y, w, h = int(boundary[0]), int(boundary[1]), int(boundary[2]), int(boundary[3])
    cv2.rectangle(image, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(image, "Tracking...", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)


cap = cv2.VideoCapture("Resources/VID_20200818_161709.mp4")

tracker = cv2.TrackerMOSSE_create()
# tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerMedianFlow_create()

_, img = cap.read()  # get initial image, now get bounding box
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img, bbox)
ok, img = cap.read()

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video = cv2.VideoWriter('Resources/geno_detect.mp4', fourcc, 30, (1080, 1920))

while ok:
    timer = cv2.getTickCount()

    ok, bbox = tracker.update(img)  # updates with a new bounding box in the next frame

    if ok:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

    #video.write(img)
    ok, img = cap.read()

cv2.destroyAllWindows()
# video.release()
