import keyboard
import threading
import asyncio
import websockets
import datetime
from time import sleep
from scripts.PathFinding import TargetUnaccessible
import numpy as np
import signal


class WebSocket(websockets.WebSocketCommonProtocol):
    logResult = ''
    #path = []
    adresse = '192.168.1.38'#'10.240.104.107'

    def __init__(self, log_window, station):
        super(WebSocket, self).__init__()
        self.cycle = 0
        self.textArea = log_window
        self.station = station
        self.path = []
        self.ready = ''

    def testOffline(self, bool):
        if bool:

            print("Path found : ")
            yCell = self.station.world._height / 2 - 100
            self.station.path_finding.getPath(self.station.robot._coordinate,(self.station.world._width-160 + self.station.world._axisX, yCell), isQr=True)
            self.station.path_finding.setActualPath([(int(294 / 5.44), int(294 / 5.44)), (int(294 / 5.44), int(109 / 5.44)),(int(610 / 5.44), int(109 / 5.44))])

    async def start_communication_web(self):

        self.testOffline(False)
        shape = self.station.world._targetZone._trueCenter
        self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,
                                                                          self.station.world._tableZone)

        async with websockets.connect(
                'ws://'+self.adresse+':8765', ping_interval=None, ping_timeout=None) as websocket:#10.240.104.107  192.168.1.38
            print("in websocket")
            if self.cycle == 0 :
                go = "go"
                await websocket.send(go)
                self.log_message(go)
            self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,
                                                                              self.station.world._tableZone)  # redetec robot

            #self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (
            #        119 + self.station.world._axisX, self.station.world._height - 100 + self.station.world._axisY + 3030))
            if self.cycle == 0:
                self.ready = await websocket.recv()
                print(self.ready)
            if self.ready == "depart":
                self.log_message(self.ready)
                print("< {ready}")
                print(self.station.world._height-175 + self.station.world._axisY)

                #await self.moveToPixel(websocket, (54*self.station.world._ratioPixelCm, 54*self.station.world._ratioPixelCm))

                await self.send_path(websocket, (54*self.station.world._ratioPixelCm, 54*self.station.world._ratioPixelCm))#fonction Charge
                await self.moveToPixel(websocket,(54 * self.station.world._ratioPixelCm, 54 * self.station.world._ratioPixelCm))

                self.station.path_finding.setActualPath([(int(294 / 5.44), int(294 / 5.44)), (int(294 / 5.44), int(109 / 5.44)),(int(610 / 5.44), int(109 / 5.44))])
                await self.AddMove(websocket, ["DE340", "DN580"], True)

                await websocket.send("fin")
                self.log_message("fin start-charge")

                self.station.thread_com_state.speak[str].emit("Charge")
                tension = await websocket.recv()
                self.log_message(tension)


                # await self.AddMove(websocket, ["DS285", "DO200"])
                #self.station.thread_com_volt.speak[str].emit(tension)
                sleep(1)
                await websocket.send("ok")
                courant = await websocket.recv()
                #self.log_message(courant)git
                #self.station.thread_com_courant.speak[str].emit(courant)
                self.station.path_finding.setActualPath([(int(294 / 5.44) + 8, int(294 / 5.44) ), (int(294 / 5.44) + 8, int(109 / 5.44)),(int(610 / 5.44)-16, int(109 / 5.44))])
                await self.AddMove(websocket, ["DS400", "DO310"], True)
                await self.moveToPixel(websocket,(54 * self.station.world._ratioPixelCm, 54 * self.station.world._ratioPixelCm))

                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,
                #                                                                   self.station.world._tableZone)  # redetec robot
                sleep(2)

                yCell = self.station.world._height/2 - 100

                await self.send_path(websocket, (self.station.world._width-170 + self.station.world._axisX, yCell), isQr = True)#fonction QR
                await self.AddMove(websocket, ["DN050"], False)


                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,self.station.world._tableZone)

                self.path.append("RH090")#add rotation
                await websocket.send(self.path[0])
                self.log_message(self.path[0])
                next = await websocket.recv()
                if next == "next":
                    self.path.remove(self.path[0])

                # if self.station.robot._coordinate[1] < self.station.world._height - 215:
                #     self.path.append("DO060")
                #     await websocket.send(self.path[0])
                #     self.log_message(self.path[0])
                #     next = await websocket.recv()
                #     if next == "next":
                #         self.path.remove(self.path[0])


                await websocket.send("fin")
                self.log_message("fin charge-QR")

                self.station.thread_com_state.speak[str].emit("Decode QR")

                QR = await websocket.recv()
                self.station.qr_Code = QR

                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame, self.station.world._tableZone)  # redetec robot
                shape = self.station.world._shapeZone._trueCenter
                corectif = self.adjustementShapeZone(shape)
                self.log_message(QR)
                self.station.thread_com_piece.speak[str].emit(QR)
                await self.send_path(websocket, corectif)#fonction zone piece
                await self.addRotation(shape, websocket) # Se retourne vers la
                await self.moveToPixel(websocket, corectif)
                await websocket.send("fin")
                self.log_message("fin QR-piece")

                self.station.thread_com_state.speak[str].emit("Recherche de piece")
                piece = await websocket.recv()
                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,self.station.world._tableZone)  # redetec robot
                sleep(1)

                print("Where do we go :")
                print("points",self.station.world._targetZone._points,QR[-1])
                shape = self.station.world._targetZone._points[int(QR[-1])]
                corectif = self.adjustementTargetZone(shape, True)
                sleep(1)
                await self.send_path(websocket, corectif)#fonction target zone
                await self.addRotation(shape, websocket) # se retourne vers la zone de dépot
                corectif = self.adjustementTargetZone(shape, False)
                await self.moveToPixel(websocket, corectif)
                await websocket.send("fin")
                self.log_message("fin piece-drop")


                self.station.thread_com_state.speak[str].emit("Depo de la piece")
                drop = await websocket.recv()
                #self.station.vision._visionController.detectRobotAndGetAngleAruco(
                    #self.station.camera_monde.frame,self.station.world._tableZone)  # redetec robot
                self.log_message(drop)
                sleep(1)
                corectif = self.adjustementTargetZone(shape, True)
                await self.moveToPixel(websocket, corectif)
                await self.send_path(websocket, (54*self.station.world._ratioPixelCm, 54*self.station.world._ratioPixelCm))#fonction depar zone
                await websocket.send("reboot")
                self.log_message("roboot")
                self.station.thread_com_state.speak[str].emit("Arrete")
                self.station.close_timer()
                self.cycle += 1

                #self.station.thread_com_volt.speak[str].emit("44")
                #self.station.thread_com_piece.speak[str].emit("blue triangle")
                #self.station.thread_com_pos.speak[str].emit("i:90:076")
                #self.station.thread_com_state.speak[str].emit("progress")
                #self.station.thread_com_image.speak[np.ndarray].emit(np.zeros((400, 200, 3), dtype=np.uint8))

    async def AddMove(self, websocket, move, comingBack):
        for i in move:
            self.path.append(i)
        while self.path:
            if not comingBack:
                self.calibration()
            sleep(2)
            await websocket.send(self.path[0])
            self.log_message(self.path[0])
            next = await websocket.recv()
            if next == "next":
                self.path.remove(self.path[0])
        sleep(1)

    def getAngleCorrection(self):

        angle = int(self.station.robot._angle) + 1
        if angle < 0 :
            angle = angle + 360
        print("Angle", angle)
        angleCorrection = 0

        if 0 <= angle <= 45:
            angleCorrection = 0 - angle
        elif 45 < angle <= 135:
            angleCorrection = 90 - angle
        elif 135 < angle <= 225:
            angleCorrection = 180 - angle
        elif 225 < angle <= 315:
            angleCorrection = 270 - angle
        elif 315 < angle <= 360:
            angleCorrection = 360 - angle

        side = "H"
        if angleCorrection > 0:
            side = "A"
        angleCorrection = abs(angleCorrection)

        if angleCorrection <= 3:
            print("NO angle")
            return ''

        angleCorrection = str(angleCorrection)

        while len(angleCorrection) is not 3:
            angleCorrection = "0" + angleCorrection
        rotCommand = "R" + side + angleCorrection
        print(rotCommand)
        return rotCommand # rota angle depart

    async def moveToPixel(self,websocket , point):
        sleep(1)
        self.station.thread_com_state.speak[str].emit("Ajustement")
        try:
            self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,self.station.world._tableZone)
        except :
            pass

        rotCommand = self.getAngleCorrection()

        if rotCommand is not '':
            self.path.append(rotCommand)
            await websocket.send(rotCommand)
            self.log_message(rotCommand)
            next = await websocket.recv()
            if next == "next":
                self.path.remove(rotCommand)

            sleep(2)

        try:
            self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,self.station.world._tableZone)
        except :
            pass

        angle = self.station.robot._angle
        if angle < 0:
            angle = angle + 360
        origin = self.station.robot._coordinate
        target = point
        deltaX = target[0] - origin[0]
        deltaY = target[1] - origin[1]

        print(deltaX)
        print(deltaY)

        movementX = int(round((deltaX / self.station.world._ratioPixelCm) * 10))
        movementY = int(round((deltaY / self.station.world._ratioPixelCm) * 10))

        print(movementX)
        print(movementY)

        leftRight = "N"
        upDown = "N"

        if  0 <= angle <= 45 or 315 < angle <= 360:
            if deltaX >= 0:
                leftRight = "O"
            if deltaX < 0 :
                 movementX = abs(movementX)
                 leftRight = "E"

        elif 45 < angle <= 135:
            if deltaX >= 0:
                leftRight = "N"
            if deltaX < 0 :
                movementX = abs(movementX)
                leftRight = "S"
        elif 135 < angle < 225:
            if deltaX >= 0:
                leftRight = "E"
            if deltaX < 0 :
                 movementX = abs(movementX)
                 leftRight = "O"
        elif 225 <= angle < 315:
            if deltaX >= 0:
                leftRight = "S"
            if deltaX < 0 :
                movementX = abs(movementX)
                leftRight = "N"

        if (movementX) < 10:
            xCommand = ('D' + leftRight + "0" + str(movementX))

        elif 9 < (movementX) < 100:
            xCommand = ('D' + leftRight + str(movementX))
        else:
            xCommand = ('D' + leftRight + str(movementX))

        print(xCommand)

        if 0 <= angle <= 45 or 315 < angle <= 360:
            if deltaY >= 0:
                upDown = "N"
            if deltaY < 0:
                movementY = abs(movementY)
                upDown = "S"

        elif 45 < angle <= 135:
            if deltaY >= 0:
                upDown = "E"
            if deltaY < 0:
                movementY = abs(movementY)
                upDown = "O"

        elif 135 < angle < 225:
            if deltaY >= 0:
                upDown = "S"
            if deltaY < 0:
                movementY = abs(movementY)
                upDown = "N"
        elif 225 <= angle < 315:
            if deltaY >= 0:
                upDown = "O"
            if deltaY < 0:
                movementY = abs(movementY)
                upDown = "E"

        if (movementY) < 10:
            yCommand = ('D' + upDown + "0" + str(movementY))

        elif 9 < (movementY) < 100:
            yCommand = ('D' + upDown + str(movementY))
        else:
            yCommand = ('D' + upDown + str(movementY))

        print(yCommand)
        self.path.append(xCommand)
        await websocket.send(xCommand)
        self.log_message(xCommand)
        next = await websocket.recv()
        if next == "next":
            self.path.remove(xCommand)

        sleep(2)

        self.path.append(yCommand)
        await websocket.send(yCommand)
        self.log_message(yCommand)
        next = await websocket.recv()
        if next == "next":
            self.path.remove(yCommand)

        sleep(2)

    async def send_path(self, websocket, destination, isQr = False):
        self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, destination, isQr)
        #self.calibration()
        sleep(2)
        self.station.thread_com_state.speak[str].emit("Mouvement")
        print(self.path)
        while not self.path:
            self.log_message("WS empty")
            sleep(2)

        while self.path:
            self.calibration()
            await websocket.send(self.path[0])
            self.log_message(self.path[0])
            next = await websocket.recv()
            if next == "next":
                self.path.remove(self.path[0])

            sleep(2)

    def calibration(self):
        self.station.thread_com_state.speak[str].emit("Calibration")
        # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,self.station.world._tableZone)  # redetec robot
        angle = int(self.station.robot._angle) + 1  # +1 correctif angle
        side = "H"
        if angle < 0:
            side = "A"
            angle = abs(angle)
        if angle<=3:
             #self.path.insert(0, "XX000")  # rota angle depart
             return
        angle = str(angle)
        while len(angle) is not 3:
            angle = "0" + angle
        self.path.insert(0, "R" + side + angle)  # rota angle depart


    async def addRotation(self, obj, websocket):
        self.calibration()
        print("obj",obj)
        if obj[0] > self.station.world._width-100:
            return
        elif obj[0]<100:
            self.path.append("RH180")
        elif obj[1] > self.station.world._height/2:
            self.path.append("RH090")
        elif obj[1] < self.station.world._height/2:
            self.path.append("RA090")
        while self.path:
            await websocket.send(self.path[0])
            self.log_message(self.path[0])
            next = await websocket.recv()
            if next == "next":
                self.path.remove(self.path[0])


    def adjustementShapeZone(self, shape):
        sx = shape[0]
        sy = shape[1]
        adjustementX = 0
        adjustementY = 0
        correctif_recul = 130
        space = 120
        if sy> self.station.world._height-space:
            adjustementY = -correctif_recul
        elif sy < space:
            adjustementY = correctif_recul
        elif sx > self.station.world._width - space:
            adjustementX = -correctif_recul
        elif sx < space:
            adjustementX = correctif_recul
        return (sx+adjustementX, sy+adjustementY)

    def adjustementTargetZone(self, shape, enApproche):
        sx = shape[0]
        sy = shape[1]
        adjustementX = 0
        adjustementY = 0
        correctif_recul = 92
        if enApproche:
            correctif_recul = 140
        space = 120
        if sy> self.station.world._height-space:
            adjustementY = -correctif_recul
        elif sy < space:
            adjustementY = correctif_recul
        elif sx > self.station.world._width - space:
            adjustementX = -correctif_recul
        elif sx < space:
            adjustementX = correctif_recul
        return (sx+adjustementX, sy+adjustementY)

    def thread_start_comm_web(self):
        t2 = threading.Thread(target=self.async_run_comm_web)
        t2.start()

    def async_run_comm_web(self):
        asyncio.run(self.start_communication_web())


    def thread_start_update_log(self):
        t4 = threading.Thread(target=self.run_update_log)
        t4.start()

    def run_update_log(self):
        while True:
            if keyboard.is_pressed('q'):
                break
            self.textArea.value = self.logResult

    def log_message(self, message):
        self.logResult += str(self.station.timer) + " : " + message + "\n"
        self.station.thread_com_log.speak[str].emit(self.logResult)
        return self.logResult

    def check_test(self):
        return self.logResult

    async def start_communication_volt(self):
        async with websockets.connect(
                'ws://'+self.adresse+':4321', ping_interval=None, ping_timeout=None) as websocket:#10.240.104.107  192.168.1.38
            await websocket.send("go")
            while True:
                volt = await websocket.recv()
                #volt = await asyncio.wait_for(websocket.recv(), timeout=1)
                self.station.thread_com_volt.speak[str].emit(volt)
                #print(volt)
                sleep(2)
                await websocket.send("next")

    def thread_start_comm_volt(self):
        t45 = threading.Thread(target=self.async_run_comm_volt)
        t45.start()

    def async_run_comm_volt(self):
        asyncio.run(self.start_communication_volt())

