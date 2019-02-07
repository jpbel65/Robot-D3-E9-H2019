import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlText
from pyforms.controls import ControlPlayer
from pyforms.controls import ControlImage
from pyforms.controls import ControlButton
import urllib.request
import matplotlib.image as mpimg
import numpy as np
import cv2
import keyboard
from PIL import Image
import threading


class BaseStation(BaseWidget):
    content = b''
    res_web = b''
    image = mpimg.imread("téléchargement.png")
    print(type(image))
    image = (image * (255, 255, 255)).astype(np.uint8)
    data = np.zeros((400, 200, 3), dtype=np.uint8)

    def __init__(self):
        super(BaseStation, self).__init__('Station de base')

        #Definition of the forms fields
        self.textArea = ControlTextArea('Log', 'Default value')
        self.textState = ControlText('État')
        self.textVolt = ControlText('Voltage')
        self.textPos = ControlText('Position')
        self.textPiece = ControlText('Pièce')
        self.textPlayer = ControlPlayer('Playground')
        self.textImage = ControlImage('Field')
        self.buttonLog = ControlButton('Log')
        self.buttonBoo = ControlButton('Boo')

        self.formset = ['', '||', 'textArea', '||',
                        (('textState', '||', 'textPiece'), '=',
                         ('textVolt', '||', 'textPos'), '=',
                         ('buttonLog', '||', 'buttonBoo'), '=',
                         ('textPlayer', '||', 'textImage')), '||', '', '=', '']

        # Define the button action
        self.buttonLog.value = self.button_action
        self.buttonBoo.value = self.buttonboo_action
        self.draw()
        self.drawrobot(8, 3)
        #self.__dedrawrobot(4, 3)

    def drawrobot(self, i, j):
        self.textPos.value = "[ i = %d to %d, j = %d to %d]" % (i, i + 1, j, j + 1)
        i = (i * 16) + 57 #121 si i = 4
        j = (j * 16) + 37 #85 si j = 3
        for k in range(i, i+31):
            for l in range(j, j+31):
                self.data[k, l] = [255, 20, 147]
        self.textImage.value = self.data


    def dedrawrobot(self, i, j):
        i = (i * 16) + 57
        j = (j * 16) + 37
        for k in range(i, i+31):
            for l in range(j, j+31):
                if k == i + 15 or l == j + 15:
                    self.data[k, l] = [0, 0, 0]
                else:
                    self.data[k, l] = [255, 255, 255]
        self.textImage.value = self.data

    def draw(self):
        idraw = [56, 72, 88, 104, 120, 136, 152, 168, 184, 200, 216, 232, 248, 264, 280, 296, 312, 328, 344]
        jdraw = [36, 52, 68, 84, 100, 116, 132, 148, 164]
        for i in range(50, 350):
            for j in range(20, 180):
                if (i-56) % 16 == 0 or (j-36) % 16 == 0:
                    self.data[i, j] = [0, 0, 0]
                else:
                    self.data[i, j] = [255, 255, 255]
        self.textImage.value = self.data

    def button_action(self):
        """Button action event"""
        self.content += self.res_web
        self.textArea.value = self.content.decode("utf-8")
        t1 = threading.Thread(target=self.callsocket)
        t1.start()




    def buttonboo_action(self):
        """Button action event"""
        t = threading.Thread(target=self.startcam)
        t.start()

    def callsocket(self):
        self.res_web = urllib.request.urlopen("http://DESKTOP-5L14B5E:6543").read() + b'\r\n'
        #self._textArea.value = self.res_web.decode("utf-8")

    def startcam(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret is True:
                self.textPlayer.frame = frame

                # Press Q on keyboard to stop recording
                if keyboard.is_pressed('q'):
                    break

            # Break the loop
            else:
                break

                # When everything done, release the video capture and video write objects
        cap.release()


#Execute the application


if __name__ == "__main__":
    pyforms.start_app(BaseStation)
