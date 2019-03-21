import cv2
import threading
from scripts.PathDrawer import PathDrawer
from scripts.PathFinding import PathFinding


class CameraMonde:
    stop = False

    def __init__(self, camera_window, world):
        self.textPlayer = camera_window
        self.drawPlannedPath = True
        self.capture = None
        self.world = world
        self.path_finding = PathFinding(self.world, 22, 22, 13, 0.2, [])#le array vide est la pour le constructeur de pathfinder
        self.path = self.getPlannedPath()

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 760)
        self.capture.set(cv2.CAP_PROP_FPS, 15)

        while True:
            ret, frame = self.capture.read()
            if ret is True:

                self.textPlayer.frame = frame

                if self.drawPlannedPath:
                    for i in self.path:
                        if i != self.path[-1]:
                            cv2.line(frame, (i[1], i[0]),
                                     (self.path[self.path.index(i) + 1][1], self.path[self.path.index(i) + 1][0]), 125,
                                     2)
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
        path = PathDrawer(self.path_finding.getTestTable())
        return path.getPixelatedPath()
