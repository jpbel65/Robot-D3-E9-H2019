from PyQt5 import QtCore
import numpy as np


class Communicate(QtCore.QObject):
    speak = QtCore.pyqtSignal((np.ndarray,), (str,))
