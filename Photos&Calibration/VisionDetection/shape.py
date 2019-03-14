import cv2
import numpy as np

big_img = cv2.imread("snapshot_1280_720_0.jpg", 1)


# define green value range
imagem = cv2.bitwise_not(big_img )
big_img_hsv = cv2.cvtColor(big_img, cv2.COLOR_BGR2HSV)
cv2.imshow("img",big_img_hsv)
#green
#mask = cv2.inRange(big_img_hsv , np.array([45, 45, 100]), np.array([80, 255, 255]))
#mask = cv2.inRange(big_img_hsv , np.array([53, 25, 45]), np.array([75, 255, 255]))
# black
mask = cv2.inRange(big_img_hsv , np.array([0, 0, 0]), np.array([180, 255, 90]))
# white
#mask = cv2.inRange(imagem , np.array([0, 0, 0]), np.array([0, 0, 255]))
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
contour_length = cv2.arcLength(contours[1], True)
polygon_points = cv2.approxPolyDP(contours[1], 0.02 * contour_length, True)
x, y, w, h = cv2.boundingRect(polygon_points)
#ok=cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)
color_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
# draw contours onto image
color_img = cv2.drawContours(color_img, contours, -1, (0, 255, 0), 2)
cv2.imshow("Contour", color_img)
#ok=cv2.Canny(ok,100,300)
#ok = cv2.GaussianBlur(ok, (1, 1), 0)
#mask1 = cv2.Canny(ok, 100, 300)
#cv2.imshow("Contour2", ok)



cv2.imshow("img2",imagem )
mask2 = cv2.inRange(imagem , np.array([0, 0, 0]), np.array([180, 255, 90]))
mask2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
mask2 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
contours2, hierarchy2 = cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
color_img2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
# draw contours onto image
color_img2 = cv2.drawContours(color_img2, contours, -1, (0, 255, 0), 2)
cv2.imshow("Contour2", color_img)
cv2.waitKey()