import cv2
import numpy as np
import math
import imutils


def blur(big_img):
    big_img = cv2.GaussianBlur(big_img, (5, 5), 0)
    big_img = cv2.medianBlur(big_img, ksize=1)

    return big_img


def canny(big_img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    cimage = cv2.morphologyEx(big_img, cv2.MORPH_OPEN, kernel=kernel, iterations=3)
    cimage = cv2.Canny(cimage, 100, 150)
    cimage = cv2.GaussianBlur(cimage, (1, 1), 0)
    # cimage = cv2.Canny(cimage, 150, 150)
    cimage = cv2.dilate(cimage, kernel)
    contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:70]
    i = -1
    for c in contours:
        i += 1
        contour_length = cv2.arcLength(c, True)
        polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
        area = cv2.contourArea(polygon_points)
        if area >= 4000 and area <= 8000 and len(polygon_points) == 4:
            print(i)
            lol = len(polygon_points)
            lololo = len(c)
            x, y, w, h = cv2.boundingRect(polygon_points)
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'zone de depot detecte', (x, y + 27), 0, 0.3, (0, 255, 0))
        elif area >= 20 and area <= 100 and len(polygon_points) == 4:
            x, y, w, h = cv2.boundingRect(polygon_points)
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'zone de depot detecte', (x, y + 27), 0, 0.3, (0, 255, 0))

    contour_length = cv2.arcLength(contours[68], True)
    polygon_points = cv2.approxPolyDP(contours[68], 0.02 * contour_length, True)
    area = cv2.contourArea(polygon_points)
    print("area")
    print(area)
    # color_img = cv2.drawContours(color_img, contours, 68, (0, 255, 0), 2 )
    cv2.imshow("Contour", color_img)
    cv2.waitKey()



def detection(big_img):
    big_img_hsv = cv2.cvtColor(big_img.copy(), cv2.COLOR_BGR2HSV)
    # cv2.imshow("img2", big_img)
    # define green value range
    # magem = cv2.bitwise_not(big_img )
    # black
    # mask = cv2.inRange(big_img_hsv, np.array([0, 0, 0]), np.array([0, 0, 255]))
    mask = cv2.inRange(big_img_hsv, np.array([0, 0, 0]), np.array([180, 255, 110]))
    # white
    # white_lower = np.array([0, 0, 60])
    # white_higher = np.array([180, 30, 100])
    lower_white_hsv = np.array([0, 0, 212])
    higher_white_hsv = np.array([131, 255, 100])
    # mask = cv2.inRange(big_img_hsv , white_lower, white_higher )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]
    x1, y1, w1, h1 = 0, 0, 0, 0
    for c in contours:
        contour_length = cv2.arcLength(c, True)
        polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
        area = cv2.contourArea(polygon_points)
        if area > 80000 and area < 130000:
            print(len(c))
            x, y, w, h = cv2.boundingRect(polygon_points)
            centerX = (x + w) / 2
            centerY = (y + h) / 2
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'zone de depart detecte', (x, y), 0, 0.3, (0, 255, 0))
        elif area >= 600000 and area < 800000:
            x, y, w, h = cv2.boundingRect(polygon_points)
            x1, y1, w1, h1 = x, y, w, h
            centerX = (x + w) / 2
            centerY = (y + h) / 2
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'table detecte', (x, y), 0, 0.3, (0, 255, 0))
        elif area > 4000 and area <= 30000:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
        # cv2.circle(color_img, center, int(radius), (0, 255, 255), 2)
    # color_img = cv2.drawContours(color_img, contours,4, (0, 255, 0), 2)
    cv2.imshow("detection", color_img)
    cv2.waitKey()
    return mask, (x1, y1, w1, h1)



def detectCircle(crop_img):
    # cv2.imshow("alreade grey ?",crop_img)
    # gray=cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
    '''kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    mask = cv2.morphologyEx(crop_img, cv2.MORPH_OPEN, kernel=kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    '''
    # cv2.imshow("in zone script",gray)
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=70, param2=20, minRadius=40, maxRadius=60)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=70, param2=20, minRadius=20, maxRadius=35)

    print(circles)
    limit = len(circles)
    circles = np.int64(np.around(circles))
    print(len(circles))
    j = 0
    base = []
    for i in circles[0, :]:
        print(j)
        # cv2.circle(crop_img, (i[0], i[1]), 40, (0, 0, 255), 15)
        base.append((i[0], i[1]))
        print(i[2])

    # cv2.imshow("wut1", crop_img)
    '''aqua = np.array([0, 255, 0], dtype=np.uint8)
    masked_img = cv2.inRange(crop_img, aqua, aqua)
    cv2.imshow("wut", masked_img)
    masked_img = cv2.bitwise_and(crop_img, crop_img, mask=masked_img)
    '''

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=70, param2=20, minRadius=40, maxRadius=60)
    circles = np.int64(np.around(circles))
    haut = []
    for i in circles[0, :]:
        print(j)
        # cv2.circle(crop_img, (i[0], i[1]), 40, (0, 255, 255), 15)
        haut.append((i[0], i[1]))
    for x in base:
        for y in haut:
            dis = math.sqrt((x[0] - y[0]) ** 2 + (y[1] - y[1]) ** 2)
            if dis <= 100:
                haut.remove(y)

    if len(haut) != 0:
        for x in haut:
            base.append(x)
    for i in base:
         pass
         #cv2.circle(crop_img, (i[0], i[1]), 40, (0, 0, 255), 10)

    cv2.imshow("CERCLE", crop_img)
    cv2.waitKey()
    return base


def detect_circles_by_colour(image):
    big_img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(big_img_hsv, np.array([0, 0, 0]), np.array([180, 255, 110]))
    cv2.imshow("masky", mask)
    output_image = cv2.bitwise_and(big_img_hsv, big_img_hsv, mask=mask)
    cv2.imshow("output_image =y", output_image)
    retval, image_binary = cv2.threshold(output_image, 50, 180, cv2.THRESH_BINARY)
    gray_image = cv2.cvtColor(image_binary, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1.2, 20,
                               param1=50, param2=25, minRadius=26, maxRadius=50)
    circles = np.uint16(np.around(circles))
    print(len(circles))
    j = 0
    for i in circles[0, :]:
        percentage_x = -1 * (i[0] - (720 / 2)) / (720 * 5)
        percentage_y = -1 * (i[1] - (1280 / 2)) / (1280 * 5)

        base_x = i[0] + int(percentage_x) * 700
        base_y = i[1] + int(percentage_y) * 1280
        cv2.circle(image, (base_x, base_y), 50, (255, 255, 0), 2)
        cv2.circle(image, (base_x, base_y), 2, (0, 0, 255), 3)
        j += 1
    cv2.waitKey()


def detectblackzone(crop_img, w1, h1):
    # cv2.line(crop_img, (0, h1), (w1 + h1, 0), (255, 0, 0), 15)
    x1, y1 = 0, 0
    cv2.line(crop_img, (x1, y1), (x1 + w1, y1), (255, 0, 0), 15)
    # cv2.line(big_img, (x1, y1), (x1, y1 + h1), (255, 0, 0), 15)
    # cv2.line(crop_img, (x1, h1), (x1 + w1, y1 +h1), (255, 0, 0), 15)
    # cv2.line(big_img, (x1 + w1, y1 + h1), (x1 + w1, y1 - h1), (255, 0, 0), 15)
    cv2.imshow("OWOW ", crop_img)

    mask = cv2.inRange(crop_img, np.array([0, 0, 0]), np.array([180, 255, 110]))
    cv2.imshow("OWOW mask  ", mask)
    cv2.waitKey()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    cimage = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=3)
    cimage = cv2.Canny(cimage, 150, 150)
    cimage = cv2.GaussianBlur(cimage, (1, 1), 0)
    cimage = cv2.Canny(cimage, 150, 150)
    cimage = cv2.dilate(cimage, kernel)
    '''
    # contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]
    x1, y1, w1, h1 = 0, 0, 0, 0
    for c in contours:
        contour_length = cv2.arcLength(c, True)
        polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
        area = cv2.contourArea(polygon_points)
        if area >= 5000 and area < 8000 and len(polygon_points) == 4:
            print("peut etre zone de piece4 ")
            print(len(polygon_points))
            x, y, w, h = cv2.boundingRect(polygon_points)
            centerX = (x + w) / 2
            centerY = (y + h) / 2
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'zone de depart detecte', (x, y), 0, 0.3, (0, 255, 0))

    # color_img = cv2.drawContours(color_img, contours, 4, (0, 255, 0), 2)
    cv2.imshow("HOPE IT WLL WORK ", color_img)
    cv2.waitKey()




def getTrianglePeak(markers):
    dis1 = math.sqrt((markers[0][0] - markers[1][0]) ** 2 + (markers[0][1] - markers[1][1]) ** 2)
    dis2 = math.sqrt((markers[0][0] - markers[2][0]) ** 2 + (markers[0][1] - markers[2][1]) ** 2)
    dis3 = math.sqrt((markers[1][0] - markers[2][0]) ** 2 + (markers[1][1] - markers[2][1]) ** 2)
    # distance_1 = euc_distance(markers[0], markers[1])
    # distance_2 = euc_distance(markers[0], markers[2])
    # distance_3 = euc_distance(markers[1], markers[2])

    if dis1 > dis2 and dis3 > dis2:
        return markers[1]
    if dis1 > dis3 and dis2 > dis3:
        return markers[0]
    else:
        return markers[2]


def DetectTableAlternative(big_img):
    mask = cv2.adaptiveThreshold(cv2.cvtColor(big_img.copy(), cv2.COLOR_BGR2GRAY), 255,
                                 cv2.THRESH_BINARY, cv2.THRESH_BINARY, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=2)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    for c in contours:
         contour_length = cv2.arcLength(c, True)
         polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
         area = cv2.contourArea(polygon_points)
         if area >= 600000 and area <= 800000:

                x, y, w, h = cv2.boundingRect(polygon_points)
                cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(color_img, 'zone de depart detecte', (x, y), 0, 0.3, (0, 255, 0))
                break

    # color_img = cv2.drawContours(color_img, contours, 0, (0, 255, 0), 2)
    #cv2.imshow("table", color_img)
    #cv2.waitKey()
    return x,y,w,h


def detectTriangleOnRobot(crop_img):
    image = cv2.GaussianBlur(crop_img, (5, 5), 0)
    image = cv2.medianBlur(image, ksize=3)
    resized = image

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny_output = cv2.Canny(resized, 150, 150)
    canny_output = cv2.GaussianBlur(canny_output, (5, 5), 0)
    canny_output = cv2.Canny(resized, 150, 150)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_OPEN, kernel=kernel)
    canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    hierachy = cv2.findContours(canny_output_close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(hierachy)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

    for c in cnts:
        M = cv2.moments(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            centerX = int((M["m10"] / M["m00"]))
            centerY = int((M["m01"] / M["m00"]))

            peak = getTrianglePeak(approx)
            dy = peak[1] - centerY
            dx = peak[0] - centerX

            angle = math.atan2(-dy, dx)
            angle = np.rad2deg(angle)
            return angle


if __name__ == "__main__":
    # execute only if run as a script
    '''capture =cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,760)
    capture.set(cv2.CAP_PROP_FPS,15)
    big_img = cv2.imread("picture_serie2_1280_720_.jpg", 1)
    while True:'''

    # v2.imshow("origian",big_img)
    # big_img= blur(big_img)
    big_img = cv2.imread("picture_serie2_1280_720_5.jpg", 1)
    x,y,w,h=DetectTableAlternative(big_img)
    x1, y1, w1, h1 = x,y,w,h


    #mask, coord = detection(big_img)
    #x1, y1, w1, h1 = coord[0], coord[1], coord[2], coord[3]
    # x1, y1, w1, h1= 25, 65, 1240, 580

    crop_img = big_img[y1:y1 + h1, x1:x1 + w1]
    #base = detectCircle(crop_img)
    canny(crop_img)
    detectblackzone(crop_img, w1, h1)

    #detectTriangleOnRobot(crop_img)
