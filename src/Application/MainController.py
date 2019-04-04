from Application.VisionController import VisionController


class MainController:

    def __init__(self):
        self._robotController = None
        self._table = None
        self._visionController = VisionController()
        self._trajectoryMapper = None
        self._trajectoryCalculator = None
        self._pieceToTakeInfo = None
        self._converter = None
        self._robot = None
        self._zoneList = None
        self._shapeList = None
        self._RobotController_ = None
        self._TrajectoryMapper_ = None
        self._ScaleConverter_ = None

    def sendMessageToRobot(self, aString_message):
        pass

    def setPieceToTakeInfo(self):
        pass

    def main(self):
        pass

    def detectWorldElement(self, image):
        world = self._visionController.detectEntities(image)
        return world
