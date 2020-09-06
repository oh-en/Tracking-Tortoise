def warp_image(image, coords):
    """
    :param image_path: path to the image that will be warped.
    :param coords: coordinates of the points to be warped. Points can be selected and found using select_points.py
    :return: returns the output warped image from a top down perspective
    """

    from numpy import float32
    from cv2 import getPerspectiveTransform, warpPerspective, imread, resize

    #image = imread(image_path)
    image = resize(image, (int(720 * 3 / 2), 720))  # maybe I don't need this

    width, height = 71*17, 24*17
    pts1 = float32(coords)
    pts2 = float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = getPerspectiveTransform(pts1, pts2)  # creates a top down image of something that was at an angle
    imgOutput = warpPerspective(image, matrix, (width, height))

    return imgOutput
