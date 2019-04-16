import cv2
import threading
from scripts.PathDrawer import PathDrawer
from scripts.PathFinding import PathFinding
from time import sleep


class CameraMonde:
    frameCount = 0
    stop = False

    def __init__(self, camera_window, station):
        self.textPlayer = camera_window
        self.station = station
        self.drawPlannedPath = True
        self.capture = None
        self.realCapture = None
        self.frame = None
        self.world = None
        self.path_finding = None
        self.path = None
        self.obstacles = None
        self.world_true = False
        self.whereTheRobotHasBeen = []


    def start_camera(self):
        self.capture = cv2.VideoCapture(1)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture.set(cv2.CAP_PROP_FPS, 15)

        while True:
                self.frameCount += 1
                ret, frame = self.capture.read()
                if ret is True:
                    self.frame = frame
                    self.showedFrame = frame.copy()
                    self.textPlayer.frame = self.showedFrame

                    if self.station.world is not None and self.world_true is False:
                        self.world = self.station.world
                        self.path_finding = self.station.path_finding
                        self.world_true = True
                    if self.world_true is True:
                        for i in self.world._obstacles:
                            cv2.circle(self.showedFrame, (i._coordinate[0] + self.world._axisX, i._coordinate[1] + self.world._axisY), i._radius, 180, 3)
                        cv2.circle(self.showedFrame,(int(self.world._shapeZone._trueCenter[0]) + self.world._axisX, int(self.world._shapeZone._trueCenter[1])+ self.world._axisY),4, (0, 0, 255), 3)
                        cv2.circle(self.showedFrame, (int(self.world._targetZone._trueCenter[0])+ self.world._axisX, int(self.world._targetZone._trueCenter[1])+ self.world._axisY), 4, (0,0,255), 3)

                    if self.station.path_finding is not None:
                        if len(self.station.path_finding.getActualPath()) > 1 :
                            for i in range (0, len(self.station.path_finding.getActualPath())-2):
                                curPoint = self.station.path_finding.getActualPath()[i]
                                thenPoint = self.station.path_finding.getActualPath()[i+1]

                                curPoint = self.convertPointInPixel(curPoint)
                                thenPoint = self.convertPointInPixel(thenPoint)

                                cv2.line(self.showedFrame,curPoint,thenPoint,(0,255,0),2)

                    if self.station.robot is not None:
                        if len(self.whereTheRobotHasBeen) > 70:
                            self.whereTheRobotHasBeen.pop(0)
                        if len(self.whereTheRobotHasBeen) > 1 :
                            for i in range(1, len(self.whereTheRobotHasBeen) - 1):
                                cur_x = int(self.whereTheRobotHasBeen[i][0])
                                cur_y = int(self.whereTheRobotHasBeen[i][1])
                                prev_x = int(self.whereTheRobotHasBeen[i - 1][0])
                                prev_y = int(self.whereTheRobotHasBeen[i - 1][1])

                                cv2.line(self.showedFrame, (prev_x, prev_y), (cur_x, cur_y), (0, 255, 255), 2)
                        cv2.circle(self.showedFrame, (int(self.station.robot._coordinate[0] + self.world._axisX),  int(self.station.robot._coordinate[1]) + self.world._axisY), 3, (0,255,0), 3)
                        # self.whereTheRobotHasBeen.append((int(self.station.robot._coordinate[0] + self.world._axisX),int(self.station.robot._coordinate[1]) + self.world._axisY))
                        if self.frameCount%3 == 0:
                            try :
                                self.whereTheRobotHasBeen.append((int(
                                    self.station.robot._coordinate[0] + self.world._axisX), int(
                                    self.station.robot._coordinate[1]) + self.world._axisY))
                                self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame, self.station.world._tableZone)

                            except :
                                continue
                    if self.stop is True:
                        break

                # Break the loop
                else:
                    break
                    # When everything done, release the video capture and video write objects

        self.capture.release()

    def nextImage(self):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 760)
        self.capture.set(cv2.CAP_PROP_FPS, 15)
        ret, frame = self.capture.read()
        return frame

    def thread_start_camera(self):
        """Button action event"""
        t = threading.Thread(target=self.start_camera)
        t.start()

    def stop_camera_thread(self):
        self.stop = True

    def getPlannedPath(self):
        pathDrawer = PathDrawer(self.path_finding)
        self.path = pathDrawer.getPixelatedPath()
        return pathDrawer.getPixelatedPath()

    def convertPointInPixel(self, point):
        newPoint = (int(point[1] * self.station.world._ratioPixelCm) + self.world._axisX, int(point[0] * self.station.world._ratioPixelCm) +  self.world._axisY)
        return newPoint