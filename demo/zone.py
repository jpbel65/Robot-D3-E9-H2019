import cv2
import numpy as np
import math
import imutils


def blur(big_img):
    big_img = cv2.GaussianBlur(big_img, (5, 5), 0)
    big_img = cv2.medianBlur(big_img, ksize=1)

    return big_img


def canny(rip, x1, y1, w1, h1 ):
    copy = cv2.cvtColor(rip.copy(), cv2.COLOR_BGR2GRAY)
    copy_bgr = cv2.cvtColor(copy.copy(), cv2.COLOR_GRAY2BGR)
    #cv2.line(big_img, (w1, 0), (w1, h1), (0, 255, 0), 8)
    #cv2.line(big_img, (0, 0), (w1, 0), (0, 255, 0), 8)
    #cv2.line(big_img, (0,0), (0, h1), (0, 255, 0), 8)
    #cv2.imshow("cimage", big_img)
    #cv2.waitKey()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cimage = cv2.morphologyEx(rip, cv2.MORPH_OPEN, kernel=kernel, iterations=3)

    cimage = cv2.Canny(cimage, 100, 150)
    cimage = cv2.GaussianBlur(cimage, (1, 1), 0)
    #cimage = cv2.Canny(cimage, 100, 150)
    cimage = cv2.dilate(cimage, kernel)
    cv2.imshow("cimage", cimage)
    cv2.waitKey()

    contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:35]
    i = -1
    centerX,centerY = 0,0
    for c in contours:
        i += 1
        contour_length = cv2.arcLength(c, True)
        polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
        area = cv2.contourArea(polygon_points)
        if area >= 4000 and area <= 8000 and len(polygon_points) == 4:
            print("boucle")
            print(area)

            M = cv2.moments(c)
            centerX = int((M["m10"] / M["m00"]))
            centerY = int((M["m01"] / M["m00"]))
            x, y, w, h = cv2.boundingRect(polygon_points)
            points = detectPointOfTargetZone(copy_bgr ,(centerX,centerY))
            if  h <=200 and  len(points) == 4:

               cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
               cv2.putText(color_img, 'zone de depot detecte', (centerX, centerY), 0, 0.3, (255, 255, 0))
            #elif h<=200  and len(points) != 4:
               # cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
              #  cv2.putText(color_img, 'zone de piece', (centerX, centerY), 0, 0.3, (255, 255, 0))
        '''
        elif  area >= 50 and area <= 200 and len(polygon_points) >= 4:
            M = cv2.moments(c)
            centerX = int((M["m10"] / M["m00"]))
            centerY = int((M["m01"] / M["m00"]))
            x, y, w, h = cv2.boundingRect(polygon_points)
            points = detectPointOfTargetZone(gray, (centerX, centerY))
            if h <= 200 and len(points) == 4:
                cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(color_img, 'zone de depot detecte', (centerX, centerY), 0, 0.3, (255, 255, 0))
        '''


    '''
    contour_length = cv2.arcLength(contours[33], True)
    polygon_points = cv2.approxPolyDP(contours[33], 0.02 * contour_length, True)
    area = cv2.contourArea(polygon_points)
    print("area")
    print(area)
    print(len(polygon_points))
    color_img = cv2.drawContours(color_img, contours, 32, (0, 255, 0), 2 )
    '''

    cv2.imshow("Contour", color_img)
    cv2.waitKey()
    return (centerX,centerY)



def detection(big_img):
    big_img_hsv = cv2.cvtColor(big_img.copy(), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(big_img_hsv, np.array([0, 0, 0]), np.array([180, 255, 110]))
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
        if area >= 600000 and area <= 800000:
            x, y, w, h = cv2.boundingRect(polygon_points)
            x1, y1, w1, h1 = x, y, w, h
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'TABLE', (x, y), 0, 0.3, (0, 255, 0))
        elif area > 80000 and area < 130000:
            print(len(c))
            x, y, w, h = cv2.boundingRect(polygon_points)
            centerX = (x + w) / 2
            centerY = (y + h) / 2
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'zone de depart detecte', (x, y), 0, 0.3, (0, 255, 0))
    cv2.imshow("detection", color_img)
    cv2.waitKey()
    return   x1, y1, w1, h1



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
        cv2.circle(crop_img, (i[0], i[1]), 40, (0, 0, 255), 15)
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
        cv2.circle(crop_img, (i[0], i[1]), 40, (0, 255, 255), 15)
        haut.append((i[0], i[1]))
    for x in base:
        for y in haut:
            dis = math.sqrt((x[0] - y[0]) ** 2 + (y[1] - y[1]) ** 2)
            if dis <= 180:
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

    cv2.line(crop_img, (x1, y1), (x1 + w1, y1), (255, 0, 0), 30)
    cv2.line(crop_img, (x1, y1), (x1, y1 + h1), (255, 0, 0), 10)
    cv2.line(crop_img, (x1+w1, y1), (x1+w1, y1 + h1), (255, 0, 0), 10)
    cv2.line(crop_img, (x1, h1), (x1 + w1, y1 +h1), (255, 0, 0), 10)
    # cv2.line(big_img, (x1 + w1, y1 + h1), (x1 + w1, y1 - h1), (255, 0, 0), 15)
    cv2.imshow("OWOW ", crop_img)
    cv2.waitKey()

    mask = cv2.inRange(crop_img, np.array([0, 0, 0]), np.array([180, 255,110]))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    cv2.imshow("mask ", mask)
    cv2.waitKey()

    # contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]
    x1, y1, w1, h1 = 0, 0, 0, 0
    #contour_length = cv2.arcLength(contours[3], True)
    #polygon_points = cv2.approxPolyDP(contours, 0.02 * contour_length, True)

    for c in contours:
        contour_length = cv2.arcLength(c, True)
        polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)

        area = cv2.contourArea(polygon_points)
        if area >= 4000 and area < 8000 and len(polygon_points) == 4:
            x, y, w, h = cv2.boundingRect(polygon_points)
            M = cv2.moments(c)
            centerX = int((M["m10"] / M["m00"]))
            centerY = int((M["m01"] / M["m00"]))
            #pixel = crop_img[centerY:centerY+1, centerX:centerX+1]
           # cv2.imshow("pixel",pixel)
            #cv2.waitKey()
            #if np.any(pixel[centerY, centerX] != 0):

              #  print("not black")
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(color_img, 'zone de piece', (centerX, centerY), 0, 0.3, (0, 255, 0))
            break


    #color_img = cv2.drawContours(color_img, contours, 3, (0, 255, 0), 2)
    cv2.imshow("HOPE IT WLL WORK ", color_img)
    cv2.waitKey()
    return  x, y, w, h




def getTrianglePeak(markers):
    dis1 = math.sqrt((markers[0][0][0] - markers[1][0][0]) ** 2 + (markers[0][0][1] - markers[1][0][1]) ** 2)
    dis2 = math.sqrt((markers[0][0][0] - markers[2][0][0]) ** 2 + (markers[0][0][1] - markers[2][0][1]) ** 2)
    dis3 = math.sqrt((markers[1][0][0] - markers[2][0][0]) ** 2 + (markers[1][0][1] - markers[2][0][1]) ** 2)
    # distance_1 = euc_distance(markers[0], markers[1])
    # distance_2 = euc_distance(markers[0], markers[2])
    # distance_3 = euc_distance(markers[1], markers[2])

    if dis1 > dis2 and dis3 > dis2:
        return markers[1][0]
    if dis1 > dis3 and dis2 > dis3:
        return markers[0][0]
    else:
        return markers[2][0]


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

                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                #cv2.drawContours(color_img, [box], 0, (255, 0, 0), 2)
                #cv2.drawContours(color_img, [box], 0, (255, 0, 0), 2)
                cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.putText(color_img, 'zone de depart detecte', (x, y), 0, 0.3, (0, 255, 0))
                break

    #color_img = cv2.drawContours(color_img, contours, -1, (0, 255, 0), 2)
    cv2.imshow("table", color_img)
    cv2.waitKey()
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
    cv2.imshow("canny_output_close", canny_output_close)
    cv2.waitKey()
    hierachy = cv2.findContours(canny_output_close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(hierachy)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    for c in cnts:
        M = cv2.moments(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            print("you here ")
            centerX = int((M["m10"] / M["m00"]))
            centerY = int((M["m01"] / M["m00"]))

            peak = getTrianglePeak(approx)
            dy = peak[1] - centerY
            dx = peak[0] - centerX

            angle = math.atan2(-dy, dx)
            angle = np.rad2deg(angle)
            print(centerX)
            print(centerY)
            print(angle)
            return angle,(centerX,centerY)


def detectPointOfTargetZone(crop_img,centerOfZone):
    #gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
    gray=crop_img
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    cimage = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel=kernel, iterations=3)
    cimage = cv2.Canny(cimage, 150, 150)
    cimage = cv2.GaussianBlur(cimage, (3, 3), 0)
    cimage = cv2.Canny(cimage, 150, 150)
    cimage = cv2.dilate(cimage, kernel)
    cv2.imshow("Point", cimage)
    cv2.waitKey()
    contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:400]
    points=[]
    for c in contours:
        M = cv2.moments(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(approx )
        centerX = int((M["m10"] / M["m00"]))
        centerY = int((M["m01"] / M["m00"]))
        disAvecCentre = math.sqrt((centerOfZone[0] - centerX) ** 2 + (centerOfZone[1] -centerY) ** 2)
        if area <=200  and area>=30 and disAvecCentre<=60:
            cv2.circle(crop_img, (centerX, centerY), 2, (0, 0, 255), 3)
            points.append((centerX,centerY))
    PointInOrder = []
    for i in range(len(points)):
        if i==0 and abs(points[i][0]-points[i][0])>=6:
            points.sort(key=lambda tup: tup[1])
        else:
            points.sort(key=lambda tup: tup[0])

    cv2.circle(crop_img, (centerOfZone[0], centerOfZone[1]), 2, (0, 0, 255), 3)
    cv2.drawContours(color_img, contours, -1, (255, 0, 0), 18)
    cv2.imshow("Contour", crop_img)
    cv2.waitKey()
    return points

    contours, hierarchy = cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    '''
    circles = cv2.HoughCircles(cimage, cv2.HOUGH_GRADIENT, 1, 80, param1=70, param2=20, minRadius=0, maxRadius=35)
    base = []
    for i in circles[0, :]:
        cv2.circle(crop_img, (i[0], i[1]), 5, (0, 0, 255), 5)
        base.append((i[0], i[1]))
    cv2.imshow("Point", crop_img)
    cv2.waitKey()
    '''


def piececouleur(crop_img):
    #mask = cv2.inRange(   cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV), np.array([15, 95, 60]), np.array([35, 255, 255]))
    #mask = cv2.inRange(cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV), np.array([90, 110, 80]), np.array([110, 255, 255]))
    #mask = cv2.inRange(cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV), np.array([40, 36, 50]), np.array([80, 255, 255]))
   # mask = cv2.inRange(cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2HSV), np.array([0, 150, 100]),
          #             np.array([15, 255, 255]))
    # cv2.imshow("jaune TwoObstacle",mask)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 1))
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=1)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=2)
    # cv2.imshow("jaune fixed", mask)
    # cv2.waitKey()
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:100]
    x1, y1, w1, h1 = 0, 0, 0, 0
    #    contour_length = cv2.arcLength(contours[3], True)
    # polygon_points = cv2.approxPolyDP(contours[3], 0.02 * contour_length, True)
    # area = cv2.contourArea(polygon_points)
    # print(area)
    for c in contours:
        contour_length = cv2.arcLength(c, True)
        polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)

        area = cv2.contourArea(polygon_points)
        if area >= 150 and area < 300:
            x, y, w, h = cv2.boundingRect(polygon_points)
            centerX = (x + w) / 2
            centerY = (y + h) / 2
            cv2.rectangle(color_img, (x, y), (x + 10, y + 10), (0, 255, 0), 2)
            cv2.putText(color_img, 'HERE YOU ARE ', (x, y + 20), 0, 0.3, (0, 255, 0))

    # color_img = cv2.drawContours(color_img, contours, 6, (0, 255, 0), 2)
    cv2.imshow("PIECES ", color_img)
    cv2.waitKey()


def detectShape():
    '''
    gray = crop_img[y:y + h, x:x + w]
    gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    canny_output = cv2.Canny(gray, 80, 30, 100)
    # canny_output = cv2.GaussianBlur(canny_output, (9, 9), 0)
    # canny_output = cv2.Canny(canny_output, 150, 150)
    cv2.imshow('canny', canny_output)
    cv2.waitKey()
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    # canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_OPEN, kernel=kernel)
    # canny_output_close = cv2.morphologyEx(canny_output, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    cnts, hierachy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cnts = imutils.grab_contours(hierachy)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1000]

    for c in cnts:

        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int((M["m10"] / M["m00"]) * 1)
            cY = int((M["m01"] / M["m00"]) * 1)
            peri = cv2.arcLength(c, True)

            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            if len(approx) == 2:
                cv2.circle(crop_img, (cX, cY), 2, (0, 0, 255), 4)
                break

        else:
            cX, cY = 0, 0
    # @ shape = detect(c)
    cv2.imshow("SHOW ME ", crop_img)
    cv2.waitKey()
    '''


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
    big_img = cv2.imread("photo_b_1280_720_4.jpg", 1)
    '''
    rgb_planes = cv2.split(big_img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    cv2.imwrite('AAAAAAAA.png', result)
    cv2.imwrite('a.png', result_norm)
    '''
    x,y,w,h=DetectTableAlternative(big_img)

    x1, y1, w1, h1 = x,y,w,h

    #coord = detection(big_img)
   # x1, y1, w1, h1 = coord[0], coord[1], coord[2], coord[3]
    # x1, y1, w1, h1= 25, 65, 1240, 580

    crop_img = big_img[y1:y1 + h1, x1:x1 + w1]




    cv2.imshow("cropped",crop_img)
    cv2.waitKey()
    #detection(big_img)
    #base = detectCircle(crop_img)
    #gray = cv2.cvtColor(crop_img.copy(), cv2.COLOR_BGR2GRAY)
    #centerOfZone =canny(crop_img, x1, y1, w1, h1 )

    #points=detectPointOfTargetZone(gray,centerOfZone)
    #print(points)
    x,y,w,h = detectblackzone(crop_img, w1, h1)
    #detectTriangleOnRobot(crop_img)
    #piececouleur(crop_img)
    #detectShape()




