import cv2
import numpy as np

def blur(big_img):
    big_img = cv2.GaussianBlur(big_img, (5, 5), 0)
    big_img = cv2.medianBlur(big_img, ksize=1)

    return big_img
def canny(big_img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cimage = cv2.morphologyEx(big_img, cv2.MORPH_OPEN, kernel=kernel ,iterations=3 )
    cimage = cv2.Canny(cimage,150, 150)
    cimage = cv2.GaussianBlur(cimage, (1, 1), 0)
    cimage = cv2.Canny(cimage, 150, 150)
    #cimage=cv2.erode(cimage,kernel)
    contours, hierarchy= cv2.findContours(cimage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    i=-1
    for c in contours:
           i+=1
           contour_length = cv2.arcLength(c, True)
           polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
           area = cv2.contourArea(polygon_points)
           if area >= 4000 and area <= 6200 and len(polygon_points) == 4:
               print(i)
               lol = len(polygon_points)
               lololo=len(c)
               x, y, w, h = cv2.boundingRect(polygon_points)
               cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
               cv2.putText(color_img, 'zone de depot detecte', (x , y+27), 0, 0.3, (0, 255, 0))

    #color_img = cv2.drawContours(color_img, contours, -1, (0, 255, 0), -1 )
    cv2.imshow("Contour", color_img)
    cv2.waitKey()
def pieces(img,coord):
    x1,y1,w1,h1=coord[0],coord[1],coord[2],coord[3]
    '''
    cv2.line(img, (x1, y1), (x1+w1, y1), (255, 0, 0), 5)
    cv2.line(img, (x1, y1), (x1 , y1+h1), (255, 0, 0), 5)
    cv2.line(img, (x1, y1+h1), (x1 + w1, y1+h1), (255, 0, 0), 5)
    cv2.line(img, (x1+w1, y1+h1), (x1 + w1, y1-h1), (255, 0, 0), 5)
    cv2.imshow("ZONE DE PIECES LIGNE ", img)
    '''

    big_img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, np.array([0, 0, 0]), np.array([180, 255, 110]))
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    for c in contours:
      contour_length = cv2.arcLength(c, True)
      polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
      area = cv2.contourArea(polygon_points)
      if area >= 15000 and area <= 16400:
         x, y, w, h = cv2.boundingRect(polygon_points)
         centerX = (x + w) / 2
         centerY = (y + h) / 2
         cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(color_img, 'zone de piece detecte', (x , y ), 0, 0.3, (0, 255, 0))
    #contour_length = cv2.arcLength(contours[2], True)
    #polygon_points = cv2.approxPolyDP(contours[2], 0.02 * contour_length, True)
   # area = cv2.contourArea(polygon_points)
    #lol= len(contours[2])
    #color_img = cv2.drawContours(color_img, contours, 2, (0, 255, 0), 2)
    cv2.imshow("ZONE DE PIECES ",  color_img)
    cv2.waitKey()

0
def DUU(big_img):
    x1,y1,w1,h1= 0,0,1225,590
    cv2.line(big_img, (x1, y1), (x1 + w1, y1), (255, 0, 0), 5)
    cv2.line(big_img, (x1, y1), (x1, y1 + h1), (255, 0, 0), 5)
    cv2.line(big_img, (x1, y1 + h1), (x1 + w1, y1 + h1), (255, 0, 0), 5)
    cv2.line(big_img, (x1 + w1, y1 + h1), (x1 + w1, y1 - h1), (255, 0, 0), 5)
    cv2.imshow("img2", big_img)
    mask = cv2.GaussianBlur(big_img.copy(), (7, 7), 0)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    mask = cv2.adaptiveThreshold(cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY), 255,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=5)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=1)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    i=0
    for c in contours:
           i+=1
           contour_length = cv2.arcLength(c, True)
           polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
           area = cv2.contourArea(polygon_points)
           if area >= 4800 and area <= 5200:
               print(i)
               lol = len(polygon_points)
               lololo=len(c)
               x, y, w, h = cv2.boundingRect(polygon_points)
               cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 2)
               cv2.putText(mask, 'zone de depot detecte', (x , y), 0, 1.5, (0, 255, 0))
           elif area >= 11500 and area <= 14500:
               x, y, w, h = cv2.boundingRect(polygon_points)
               centerX = (x + w) / 2
               centerY = (y + h) / 2
               cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
               cv2.putText(color_img, 'zone de piece detecte', (x, y), 0, 0.3, (0, 255, 0))




    contour_length = cv2.arcLength(contours[4], True)
    polygon_points = cv2.approxPolyDP(contours[4], 0.02 * contour_length, True)
    area = cv2.contourArea(polygon_points)
   # '''

    color_img = cv2.drawContours(big_img, contours,0, (0, 255, 0), 2)

    #color_img = cv2.drawContours(mask, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Contour",color_img)
    cv2.waitKey()
    # draw contours onto image
    return 0

def detection(big_img):

    big_img_hsv = cv2.cvtColor(big_img.copy(), cv2.COLOR_BGR2HSV)
    cv2.imshow("img2", big_img)
    # define green value range
    # magem = cv2.bitwise_not(big_img )
    # black
    mask = cv2.inRange(big_img_hsv, np.array([0, 0, 0]), np.array([180, 255, 110]))
    # white
    # ower_white_hsv = np.array([22, 22, 22])
    # higher_white_hsv = np.array([255, 255, 255])
    # mask = cv2.inRange(big_img_hsv ,lower_white_hsv, higher_white_hsv )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    x1,y1,w1,h1=0,0,0,0
    for c in contours:
      contour_length = cv2.arcLength(c, True)
      polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
      area = cv2.contourArea(polygon_points)
      if area > 80000 and area <130000:
         print(len(c))
         x, y, w, h = cv2.boundingRect(polygon_points)
         centerX = (x + w) / 2
         centerY = (y + h) / 2
         cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(color_img, 'zone de depart detecte', (x, y), 0, 0.3, (0, 255, 0))
      elif area >= 600000 and area < 800000:
         x, y, w, h = cv2.boundingRect(polygon_points)
         x1, y1, w1, h1 =x, y, w, h
         centerX = (x + w) / 2
         centerY = (y + h) / 2
         cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(color_img, 'table detecte', (x, y), 0, 0.3, (0, 255, 0))
      elif area > 4000 and area <= 30000:
          ((x, y), radius) = cv2.minEnclosingCircle(c)
          center = (int(x), int(y))
          cv2.circle(color_img, center, int(radius), (0, 255, 255), 2)
    #color_img = cv2.drawContours(color_img, contours, 1, (0, 255, 0), 2)
    cv2.imshow("Contour", color_img)
    cv2.waitKey()
    return mask ,(x1, y1, w1, h1)
# contour_length = cv2.arcLength(contours[10], True)
# polygon_points = cv2.approxPolyDP(contours[10], 0.02 * contour_length, True)
# x, y, w, h = cv2.boundingRect(polygon_points)
# area=cv2.contourArea(polygon_points)
# poitn=len(polygon_points)

# draw contours onto image
# color_img = cv2.drawContours(color_img, contours, 10, (0, 255, 0), 2)
# cv2.rectangle(color_img,(x,y),(x+w,y+h),(0,255,0),2)
# centerX= (x+w)/2
# enterY= (y+h)/2
# cv2.putText(color_img,'Moth Detected',(centerX+40,centerY+50),0,0.3,(0,255,0))
# cv2.imshow("Contour", color_img)
# draw contours onto image
if __name__ == "__main__":
    # execute only if run as a script
    big_img = cv2.imread("snapshot_1280_720_0.jpg", 1)
    blurred= blur(big_img)
    mask ,coord = detection(big_img)
    x1, y1, w1, h1 = coord[0], coord[1], coord[2], coord[3]
    crop_img = big_img[y1:y1 + h1, x1:x1 + w1]
    #pieces( cv2.cvtColor(big_img.copy(), cv2.COLOR_BGR2HSV), coord)
   # pieces(crop_img, coord)
    canny(crop_img)


