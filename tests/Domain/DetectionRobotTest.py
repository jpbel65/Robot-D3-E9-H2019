import unittest
import numpy as np
import cv2

from Domain.RobotDetector import RobotDetector
from Domain.RobotDetector import RobotNotFoundError
from Application.VisionController import VisionController

def crop_img(big_img):
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
            # cv2.drawContours(color_img, [box], 0, (255, 0, 0), 2)
            # cv2.drawContours(color_img, [box], 0, (255, 0, 0), 2)
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.putText(color_img, 'zone de depart detecte', (x, y), 0, 0.3, (0, 255, 0))
            break
    crop_img = big_img[y:y + h, x:x + w]
    return crop_img

class RobotDetectionTest(unittest.TestCase):
    def test_given_an_image_with_robot_it_returns_the_robot_position(self):
        robotDetector = RobotDetector()
        image_with_robot = cv2.imread('photo_1280_720_1.jpg')
        image_with_robot_cropped = crop_img(image_with_robot)
        expected_robot_position = (293, 320)

        angle, center = robotDetector.detect(image_with_robot_cropped)
        self.assertEqual(expected_robot_position, center)
    def test_given_an_image_without_robot_raise_error(self):
        robotDetector = RobotDetector()
        image_with_robot = cv2.imread('picture_3_1280_720_rip0.jpg')
        image_with_robot_cropped = crop_img(image_with_robot)
        self.assertRaises(RobotNotFoundError)

    def test_given_an_image_with_robot_parallel_to_axes_it_returns_the_right_robot_angle(self):
        robotDetector = RobotDetector()
        image_with_robot = cv2.imread('photo_1280_720_1.jpg')
        image_with_robot_cropped = crop_img(image_with_robot)
        angle, center = robotDetector.detect(image_with_robot_cropped)

        self.assertTrue(-10 <= angle <= 10)
    def test_given_an_image_with_robot_it_returns_the_right_robot_angle(self):
        robotDetector = RobotDetector()
        image_with_robot = cv2.imread('robotAngle.jpg')
        image_with_robot_cropped = crop_img(image_with_robot)
        angle, center = robotDetector.detect(image_with_robot_cropped)
        print(angle)
        self.assertTrue(-75 <= angle <=85)




if __name__ == '__main__':
    unittest.main()