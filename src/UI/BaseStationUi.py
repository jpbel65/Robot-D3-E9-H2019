import os
import threading
import time
from time import sleep
import cv2

import numpy as np
import pyforms
from PyQt5 import QtCore
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlImage
from pyforms.controls import ControlPlayer
from pyforms.controls import ControlText
from pyforms.controls import ControlTextArea

from Application.MainController import MainController
from Domain.Obstacle import Obstacle
from Domain.Robot import Robot
from Domain.TableZone import TableZone
from Domain.World import World
from Domain.ZoneDetector import TableZoneNotFoundError
from Domain.ZoneDetector import TargetZoneNotFoundError
from Domain.ZoneDetector import StartZoneNotFoundError
from Domain.ZoneDetector import ShapeZoneNotFoundError
from Domain.ZoneDetector import fakeAZoneList
from Domain.RobotDetector import RobotNotFoundError
from UI.CameraMondeVideoFeed import CameraMonde
from UI.Communication import Communicate
from UI.MapRender import DrawPlayground
from UI.WebSockeCommunicationt import WebSocket
from scripts.PathFinding import PathFinding


class BaseStation(BaseWidget, QtCore.QObject):
    thread_off = False
    timer_off = False
    imagetest = "picture_1280_720_0FLECHE.jpg"
    timer = 0

    def __init__(self):
        super(BaseStation, self).__init__('Station de base')

        self.robot = None

        #Definition of the forms fields
        self.textArea = ControlTextArea('Log')
        self.textTimer = ControlText('Timer')
        self.textState = ControlText('État')
        self.textVolt = ControlText('Voltage')
        self.textCourant = ControlText('Courant')#slot courant
        self.textPos = ControlText('Position')
        self.textPiece = ControlText('Pièce')
        self.textPlayer = ControlPlayer('Playground')
        self.textImage = ControlImage('Field')
        self.buttonLog = ControlButton('Log')
        self.buttonReset = ControlButton('Reset')

        self.formset = ['', '||', 'textArea', '||',
                        (('textState', '||', 'textPiece'), '=',
                         ('textVolt', '||', 'textCourant'), '=',
                         ('textPos', '||', 'textTimer'), '=',
                         ('buttonLog', '||', 'buttonReset'), '=',
                         ('textPlayer', '||')), '||', '', '=', '']

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
        self.thread_com_timer = Communicate()
        self.thread_com_timer.speak[str].connect(self.update_timer)
        self.thread_com_courant = Communicate()
        self.thread_com_courant.speak[str].connect(self.update_courant)

        self.vision = MainController()
        self.web_socket = WebSocket(self.textArea, self)


        # debut visison/pathfinding
        self.camera_monde = CameraMonde(self.textPlayer, self)
        self.camera_monde.thread_start_camera()

        self.draw_playgroung = DrawPlayground(self.textImage, self.textPos)

        self.draw_playgroung.draw_robot(8, 3)
        self.world = None
        self.image = None
        self.path_finding = None

    def button_log_action(self):
        self.image = self.camera_monde.frame
        try:

            self.world = self.vision.detectWorldElement(self.image)
            self.path_finding = PathFinding(self.world, self.web_socket.path)
            table= self.world._tableZone

            image=self.camera_monde.frame
            #crop_img = image[y1:y1 + h1, x1:x1 + w1]
           # cv2.imshow("crop_img_basestation", crop_img)
           # cv2.waitKey()

            self.vision._visionController.detectRobotAndGetAngleAruco(image, table)
            self.robot = self.vision._visionController._robot
            self.thread_start_timer()
            self.web_socket.thread_start_comm_web()
            self.web_socket.thread_start_comm_volt()

        except TargetZoneNotFoundError:
            self.web_socket.log_message("ERROR : Target Zone not Found !")
        except ShapeZoneNotFoundError:
            self.web_socket.log_message("ERROR : Shape Zone not Found !")
        except TableZoneNotFoundError:
            self.web_socket.log_message("ERROR : Table not detected !")
        except StartZoneNotFoundError:
            self.web_socket.log_message("ERROR : Target Zone not Found !")
        except ConnectionRefusedError:
            self.web_socket.log_message("ERROR : Connection Refused")
        except RobotNotFoundError:
            self.web_socket.log_message("ERROR : Robot not found !")






    def button_reset_action(self):
        print("reset")
        #self.web_socket.thread_start_comm_volt()
        #return_data = self.draw_playgroung.de_draw_robot(8, 3)
        #self.draw_playgroung.post_playgroung(return_data)

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

    @QtCore.pyqtSlot(str, name='update_timer')
    def update_timer(self, timer):
        self.textTimer.value = timer

    @QtCore.pyqtSlot(str, name='update_courant')
    def update_courant(self, courant):
        self.textCourant.value = courant

    def thread_start_timer(self):
        """Button action event"""
        t5 = threading.Thread(target=self.start_timer)
        t5.start()

    def start_timer(self):
        start = np.around(time.time())
        while True:
            if self.thread_off is True or self.timer_off is True:
                break
            now = np.around(time.time())
            self.timer = now-start
            self.thread_com_timer.speak[str].emit(str(now-start))
            sleep(1)

    def before_close_event(self):
        self.camera_monde.stop_camera_thread()
        self.thread_off = True

    def close_timer(self):
        self.timer_off = True

    def getImage(self):
        return self.camera_monde.nextImage()


# Execute the application


if __name__ == "__main__":
    pyforms.start_app(BaseStation)
