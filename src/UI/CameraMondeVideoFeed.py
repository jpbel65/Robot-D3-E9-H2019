import cv2
import threading
from scripts.PathDrawer import PathDrawer
from scripts.PathFinding import PathFinding


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


    def start_camera(self):
        self.capture = cv2.VideoCapture(1)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture.set(cv2.CAP_PROP_FPS, 15)

        while True:
                self.frameCount += 1
                ret, frame = self.capture.read()
                if ret is True:
                    self.textPlayer.frame = frame
                    self.frame = frame

                    if self.station.world is not None and self.world_true is False:
                        self.world = self.station.world
                        self.path_finding = self.station.path_finding
                        self.world_true = True
                    if self.world_true is True:
                        for i in self.world._obstacles:
                            cv2.circle(self.frame, (i._coordinate[0] + self.world._axisX, i._coordinate[1] + self.world._axisY), i._radius, 180, 3)
                        cv2.circle(self.frame,(int(self.world._shapeZone._trueCenter[0]), int(self.world._shapeZone._trueCenter[1])),4, (0, 0, 255), 3)
                        cv2.circle(self.frame, (int(self.world._targetZone._trueCenter[0]), int(self.world._targetZone._trueCenter[1])), 4, (0,0,255), 3)
                    if self.station.robot is not None:
                        cv2.circle(self.frame, (int(self.station.robot._coordinate[0]),  int(self.station.robot._coordinate[1])), 20, 40, 2)
                        # cv2.circle(self.frame, self.world._tableZone.origin, 4, (0, 0, 255),3)
                        # cv2.circle(self.frame, (self.world._tableZone.origin[0]+ self.world._tableZone.width, self.world._tableZone.origin[1]+ self.world._tableZone.height), 4, (0, 0, 255),3)
                        # cv2.circle(self.frame, (int(self.world._tableZone.origin[0]+ self.world._tableZone.width/2), int(self.world._tableZone.origin[1]+ self.world._tableZone.height/2)), 10, (0, 0, 255),3)
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
