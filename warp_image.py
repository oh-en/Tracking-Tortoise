def warp_image(image_path, coords):
    from numpy import float32
    from cv2 import getPerspectiveTransform, warpPerspective, imread, resize

    image = imread(image_path)

    image = imread(image_path)
    image = resize(image, (int(720 * 3 / 2), 720))  ## maybe I don't need this

    width, height = 1200, 400
    pts1 = float32(coords)
    pts2 = float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = getPerspectiveTransform(pts1, pts2)  # creates a top down image of something that was at an angle
    imgOutput = warpPerspective(image, matrix, (width, height))

    return imgOutput