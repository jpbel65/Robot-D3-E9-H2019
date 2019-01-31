import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlText
from pyforms.controls import ControlImage
from pyforms.controls import ControlButton
import urllib.request
import matplotlib.image as mpimg
import numpy as np


class BaseStation(BaseWidget):
    content = b''
    image = mpimg.imread("téléchargement.png")
    image = (image * 255).astype(np.uint8)

    def __init__(self):
        super(BaseStation, self).__init__('Station de base')

        #Definition of the forms fields
        self._textArea = ControlTextArea('Log', 'Default value')
        self._textState = ControlText('État')
        self._textVolt = ControlText('Voltage')
        self._textPos = ControlText('Position')
        self._textPiece = ControlText('Pièce')
        self._textImage = ControlImage('Playground')
        self._buttonLog = ControlButton('Log')
        self._buttonBoo = ControlButton('Boo')

        self.formset = ['', '||', '_textArea', '||',
                        (('_textState', '||', '_textPiece'), '=',
                         ('_textVolt', '||', '_textPos'), '=',
                         ('_buttonLog', '||', '_buttonBoo'), '=',
                         '_textImage'), '||', '', '=', '']

        # Define the button action
        self._buttonLog.value = self.__button_action
        self._buttonBoo.value = self.__buttonboo_action
        self._textImage.value = self.image

    def __button_action(self):
        """Button action event"""
        self.content += urllib.request.urlopen("http://DESKTOP-5L14B5E:6543").read() + b'\r\n'
        self._textArea.value = self.content.decode("utf-8")

    def __buttonboo_action(self):
        """Button action event"""
        urllib.request.urlopen("http://DESKTOP-5L14B5E:6543/boo").read()


#Execute the application


if __name__ == "__main__":
    pyforms.start_app(BaseStation)
