import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlText
from pyforms.controls import ControlPlayer
from pyforms.controls import ControlImage
from pyforms.controls import ControlButton

from WebSocket import WebSocket
from CameraMonde import CameraMonde
from DrawPlayground import DrawPlayground


import urllib.request


class BaseStation(BaseWidget):

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
        #self.textImage = data_return
        #self.draw_playgroung.de_draw_robot(8, 3)

    def button_log_action(self):
        self.web_socket.thread_start_comm_web()

    def button_reset_action(self):
        print("reset")

    def callsocket(self):
        self.res_web = urllib.request.urlopen("http://DESKTOP-5L14B5E:6543").read() + b'\r\n'
        #self._textArea.value = self.res_web.decode("utf-8")

    def before_close_event(self):
        self.camera_monde.stop_camera_thread()


#Execute the application


if __name__ == "__main__":
    pyforms.start_app(BaseStation)
