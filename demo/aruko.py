import cv2

import numpy as np
import cv2.aruco as aruco
import math

calib_path = ""
id_to_find = 5
marker_size = 5.5  # - [cm]
camera_matrix = np.loadtxt(calib_path + 'cameraMatrix.txt', delimiter=',')
camera_distortion = np.loadtxt(calib_path + 'cameraDistortion.txt', delimiter=',')
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()
img = cv2.imread("markerangle.jpg", 1)
capture =cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,760)
capture.set(cv2.CAP_PROP_FPS,15)
big_img = cv2.imread("picture_6_1280_720_robot4.jpg", 1)
while True:
             ret,frame=cv2.capture()
             color=cv2.cvtColor(frame.copy(), cv2.COLOR_GRAY2BGR)
             corners, ids, rejected = aruco.detectMarkers(image=frame, dictionary=aruco_dict, parameters=parameters,
                                             cameraMatrix=camera_matrix, distCoeff=camera_distortion)
             ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
             cv2.circle(color, (corners[0][0][0][0], corners[0][0][0][1]),2, (0, 0, 255), 15)
             cv2.circle(color, (corners[0][0][1][0], corners[0][0][1][1]),2, (0, 0, 255), 15)
             cv2.circle(color, (corners[0][0][2][0], corners[0][0][2][1]),2, (0, 0, 255), 15)
             cv2.circle(color, (corners[0][0][3][0], corners[0][0][3][1]),2, (0, 0, 255), 15)
             centerX=(corners[0][0][0][0]+corners[0][0][1][0]+corners[0][0][2][0]+corners[0][0][3][0])/4
             centerY=(corners[0][0][0][1]+corners[0][0][1][1]+corners[0][0][2][1]+corners[0][0][3][1])/4
             dx =  corners[0][0][0][0] - centerX
             dy= corners[0][0][0][1] -centerY
             angle = math.atan2(-dy, dx)
             angle = np.rad2deg(angle)