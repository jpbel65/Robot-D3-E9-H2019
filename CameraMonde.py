import cv2
import threading


class CameraMonde:
    stop = False

    def __init__(self, camera_window):
        self.textPlayer = camera_window

    def start_camera(self):
        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()
            if ret is True:

                self.textPlayer.frame = frame

                if self.stop is True:
                    break

            # Break the loop
            else:
                break

                # When everything done, release the video capture and video write objects
        capture.release()

    def thread_start_camera(self):
        """Button action event"""
        t = threading.Thread(target=self.start_camera)
        t.start()

    def stop_camera_thread(self):
        self.stop = True
