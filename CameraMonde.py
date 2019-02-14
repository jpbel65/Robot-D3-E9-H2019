import cv2
import keyboard
import threading


class CameraMonde:

    def __init__(self, camera_window):
        self.textPlayer = camera_window

    def start_camera(self):
        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()
            if ret is True:
                self.textPlayer.frame = frame

                # Press Q on keyboard to stop recording
                if keyboard.is_pressed('q'):
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
