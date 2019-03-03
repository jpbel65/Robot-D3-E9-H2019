import cv2
import threading


class CameraMonde:
    stop = False

    def __init__(self, camera_window):
        self.textPlayer = camera_window
        self.capture =None

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1200);
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 760);
        self.capture.set(cv2.CAP_PROP_FPS, 15)

        while True:
            ret, frame = self.capture.read()
            if ret is True:

                self.textPlayer.frame = frame

                if self.stop is True:
                    break

            # Break the loop
            else:
                break

                # When everything done, release the video capture and video write objects
        self.capture.release()

    def nextImage(self):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1200);
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 760);
        self.capture.set(cv2.CAP_PROP_FPS, 15)
        ret,frame=self.capture.read()
        return frame


    def thread_start_camera(self):
        """Button action event"""
        t = threading.Thread(target=self.start_camera)
        t.start()

    def stop_camera_thread(self):
        self.stop = True
