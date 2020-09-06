def select_points(og_image):
    """
    :param image_path: takes in the path to an image. Allows you to select points
    at the corners of the image. The points should be selected in order top left, top right, bottom left,
    bottom right. Press 'a' between each selection to confirm the choice.
    :return: Returns the coordinates of the corner images and a warped image.
    """

    import cv2
    import numpy as np

    def draw_circle(event, x, y, flags, param):

        global mouseX, mouseY

        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(img, (x, y), 7, (255, 0, 0), 2)
            mouseX, mouseY = x, y

    # img = cv2.imread(image_path)
    img = cv2.resize(og_image, (int(720 * 3 / 2), 720))  ## maybe I don't need this

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)

    coords = []

    while True:
        cv2.imshow('image', img)
        cv2.putText(img, "Pick your points, left -> right, top -> bottom. Press 'a' between points", (75, 75),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255), 2)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('a'):
            coords.append([mouseX, mouseY])
            print(coords)

    width, height = 71*17, 24*17
    pts1 = np.float32(coords)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)  # creates a top down image of something that was at an angle
    imgOutput = cv2.warpPerspective(img, matrix, (width, height))

    cv2.imshow("image", img)
    cv2.imshow("Warped", imgOutput)

    cv2.waitKey(0)

    return coords, imgOutput

# path = "Resources/IMG_20200825_132443.jpg"
# coords, warped = select_points(path)
# print(coords)
