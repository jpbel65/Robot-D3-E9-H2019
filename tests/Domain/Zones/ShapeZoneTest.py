import unittest
import cv2
import os
from Domain.ZoneDetector import ZoneDetector
from Domain.ZoneDetector import ShapeZoneNotFoundError
from Domain.HSVColorsAndConfig import *
from os import listdir, path
from os.path import isfile, join


class LocalDirectoryImageRepository():

    def __init__(self, directory_path: str):
        self.directory = directory_path
        self.files = [f for f in listdir('.') if isfile(join(self.directory, f))]
        self.current_file = path.basename(self.files[0])
        self.files.sort()



    def get_next_image(self):
        found= True
        next_file = self.files.pop()
        file_name = join(self.directory, next_file)

        if file_name =="ShapeZoneTest.py"  or file_name=="TargetZoneTest.py" or file_name =="__init__.py":
            found= False
        elif file_name=="ShapeZoneNotFound.jpg":
            found= False
        self.current_file = path.basename(file_name)
        return cv2.imread(file_name),found

    def get_current_file(self):
        return self.current_file

    def more_images(self):
        return self.files


TRAINING_DATA_DIRECTORY = ""
test_data = LocalDirectoryImageRepository(TRAINING_DATA_DIRECTORY)

def table (image):
    cimage=cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(cimage, LOWER_BLACK_HSV, UPPER_BLACK_HSV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=kernel, iterations=3)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    found = False
    for c in contours:
        contour_length = cv2.arcLength(c, True)
        polygon_points = cv2.approxPolyDP(c, 0.02 * contour_length, True)
        area = cv2.contourArea(polygon_points)
        if area >= MIN_TABLE_AREA and area < MAX_TABLE_AREA:
            x, y, w, h = cv2.boundingRect(polygon_points)
            return x,y,w,h

    if found ==False:
        print("TwoObstacle")


class MAKETHISWORK(unittest.TestCase):
    def test_ShapeZone_is_Detected_in_Batch(self):
        test_data.__init__(TRAINING_DATA_DIRECTORY)
        while test_data.more_images():
            zoneDetector =  ZoneDetector()
            data,found = test_data.get_next_image()
            if found ==False:
               pass
            else:

               x,y,w,h = table(data)
               crop_img = data[y:y+h , x:x + w]
               shapeZone = zoneDetector.detectShapeZone(crop_img,w,h)



    def test_with_image_without_shape_zone_then_it_raises_error(self):
        image= cv2.imread("ShapeZoneNotFound.jpg",1)
        zoneDetector = ZoneDetector()
        x, y, w, h = table(image)
        crop_img = image[y:y + h, x:x + w]
        shapeZone = zoneDetector.detectShapeZone(crop_img, w, h)
        self.assertRaises(ShapeZoneNotFoundError)




if __name__ == '__main__':
    unittest.main()
