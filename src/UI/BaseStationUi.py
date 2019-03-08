import pyforms
import cv2
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlText
from pyforms.controls import ControlPlayer
from pyforms.controls import ControlImage
from pyforms.controls import ControlButton

from src.UI.WebSockeCommunicationt import WebSocket
from src.UI.CameraMondeVideoFeed import CameraMonde
from src.UI.MapRender import DrawPlayground
import urllib.request


class BaseStationUi(BaseWidget):

    def __init__(self):
        super(BaseStationUi, self).__init__('Station de base')

        # Definition of the forms fields
        self.textArea = ControlTextArea('Log', 'Default value')
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

        self.web_socket = WebSocket(self.textArea)
        self.camera_monde = CameraMonde(self.textPlayer)
        self.camera_monde.thread_start_camera()
        self.draw_playgroung = DrawPlayground(self.textImage, self.textPos)

        self.draw_playgroung.draw_robot(8, 3)

    def start(self):
        pass

    def stop(self):
        pass

    def startTime(self):
        pass

    def stopTime(self):
        pass

    def button_log_action(self):
        self.web_socket.thread_start_comm_web()

    def button_reset_action(self):
        image = BaseStationUi.getImage()
        cv2.imshow("capture", image)
        print("reset")

    def callsocket(self):
        self.res_web = urllib.request.urlopen("http://DESKTOP-5L14B5E:6543").read() + b'\r\n'

    # self._textArea.value = self.res_web.decode("utf-8")

    def before_close_event(self):
        self.camera_monde.stop_camera_thread()

    def getImage(self):
        return self.camera_monde.nextImage()


# Execute the application


if __name__ == "__main__":
    pyforms.start_app(BaseStationUi)
