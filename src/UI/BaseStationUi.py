import pyforms
import cv2
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlText
from pyforms.controls import ControlPlayer
from pyforms.controls import ControlImage
from pyforms.controls import ControlButton


from UI.Communication import Communicate
from UI.WebSockeCommunicationt import WebSocket
from UI.CameraMondeVideoFeed import CameraMonde
from UI.MapRender import DrawPlayground
from Application.MainController import MainController


import numpy as np
from PyQt5 import QtCore, QtGui
import keyboard
from time import sleep
import threading


class BaseStation(BaseWidget, QtCore.QObject):
    data_log = True

    def __init__(self):
        super(BaseStation, self).__init__('Station de base')

        #Definition of the forms fields
        self.textArea = ControlTextArea('Log')
        self.textState = ControlText('État')
        self.textVolt = ControlText('Voltage')
        self.textPos = ControlText('Position')
        self.textPiece = ControlText('Pièce')
        self.textPlayer = ControlPlayer('Playground')
        self.textImage = ControlImage('Field')
        self.buttonLog = ControlButton('Log')
        self.buttonReset = ControlButton('Reset')

        self.formset = ['', '||', 'textArea', '||',
                        (('textState', '||', 'textPiece'), '=',
                         ('textVolt', '||', 'textPos'), '=',
                         ('buttonLog', '||', 'buttonReset'), '=',
                         ('textPlayer', '||', 'textImage')), '||', '', '=', '']

        # Define the button action
        self.buttonLog.value = self.button_log_action
        self.buttonReset.value = self.button_reset_action

        # Define communication entre les thread
        self.thread_com_log = Communicate()
        self.thread_com_log.speak[str].connect(self.update_log)
        self.thread_com_state = Communicate()
        self.thread_com_state.speak[str].connect(self.update_state)
        self.thread_com_volt = Communicate()
        self.thread_com_volt.speak[str].connect(self.update_volt)
        self.thread_com_pos = Communicate()
        self.thread_com_pos.speak[str].connect(self.update_pos)
        self.thread_com_piece = Communicate()
        self.thread_com_piece.speak[str].connect(self.update_piece)
        self.thread_com_image = Communicate()
        self.thread_com_image.speak[np.ndarray].connect(self.update_image)

        self.web_socket = WebSocket(self.textArea, self)
        self.camera_monde = CameraMonde(self.textPlayer)
        self.camera_monde.thread_start_camera()
        self.draw_playgroung = DrawPlayground(self.textImage, self.textPos)
        self.vision = MainController

        self.draw_playgroung.draw_robot(8, 3)

    def button_log_action(self):
        self.web_socket.thread_start_comm_web()

    def button_reset_action(self):
        image = self.getImage
        self.vision.detectWorldElement(image)
        #cv2.imshow("capture", image)
        print("reset")
        return_data = self.draw_playgroung.de_draw_robot(8, 3)
        self.draw_playgroung.post_playgroung(return_data)

    @QtCore.pyqtSlot(str, name='update_log')
    def update_log(self, text):
        self.textArea.value = text

    @QtCore.pyqtSlot(str, name='update_state')
    def update_state(self, text):
        self.textState.value = text

    @QtCore.pyqtSlot(str, name='update_volt')
    def update_volt(self, text):
        self.textVolt.value = text

    @QtCore.pyqtSlot(str, name='update_pos')
    def update_pos(self, text):
        self.textPos.value = text

    @QtCore.pyqtSlot(str, name='update_piece')
    def update_piece(self, text):
        self.textPiece.value = text

    @QtCore.pyqtSlot(np.ndarray, name='update_image')
    def update_image(self, image):
        self.textImage.value = image

    def before_close_event(self):
        self.camera_monde.stop_camera_thread()
        self.data_log = False

    def getImage(self):
        return self.camera_monde.nextImage()


# Execute the application


if __name__ == "__main__":
    pyforms.start_app(BaseStation)
