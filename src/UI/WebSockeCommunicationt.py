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
        self.textArea = log_window
        self.station = station
        self.path = []

    def testOffline(self, bool):
        if bool:
            self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,
                                                                              self.station.world._tableZone)

            print("Path found : ")
            self.station.path_finding.getPath(self.station.robot._coordinate,
                                                               (self.station.world._width/2, self.station.world._height/2))

            print(self.station.path_finding.getActualPath())
            print("Confusion is here")

    async def start_communication_web(self):

        self.testOffline(False)
        shape = self.station.world._targetZone._trueCenter
        corectif = self.adjustement(shape)
        self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,
                                                                          self.station.world._tableZone)

        async with websockets.connect(
                'ws://'+self.adresse+':8765', timeout=300) as websocket:#10.240.104.107  192.168.1.38
            print("in websocket")
            go = "go"
            await websocket.send(go)
            self.log_message(go)
            self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,
                                                                              self.station.world._tableZone)  # redetec robot

            print("Obstacle :")
            print(self.station.world._obstacles[0]._coordinate)
            print("Destination :")
            print(self.station.world._width-300 + self.station.world._axisX)
            print(self.station.world._height/2 + self.station.world._axisY)
            print("Position Robot :")
            print(self.station.robot._coordinate)
            print("Angle Robot : ")
            print((self.station.robot._angle))
            print("TABLE")
            print(self.station.world._height)
            print(self.station.world._width)

            #self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (
            #        119 + self.station.world._axisX, self.station.world._height - 100 + self.station.world._axisY + 3030))
            print(self.path)
            ready = await websocket.recv()
            print(ready)
            if ready == "depart":
                self.log_message(ready)
                print("< {ready}")
                print(self.station.world._height-175 + self.station.world._axisY)

                await self.send_path(websocket, (54*self.station.world._ratioPixelCm, 54*self.station.world._ratioPixelCm))#fonction Charge

                await self.AddMove(websocket, ["DE340", "DN580"])

                await websocket.send("fin")
                self.log_message("fin start-charge")

                self.station.thread_com_state.speak[str].emit("Charge")
                tension = await websocket.recv()
                self.log_message(tension)


                # await self.AddMove(websocket, ["DS285", "DO200"])

                #self.station.thread_com_volt.speak[str].emit(tension)
                sleep(5)
                await websocket.send("ok")
                courant = await websocket.recv()
                #self.log_message(courant)
                #self.station.thread_com_courant.speak[str].emit(courant)
                await self.AddMove(websocket, ["DS400", "DO310"])

                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,
                #                                                                   self.station.world._tableZone)  # redetec robot

                yCell = self.station.world._height/2 - 100

                await self.send_path(websocket, (self.station.world._width-160 + self.station.world._axisX, yCell))#fonction QR


                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,self.station.world._tableZone)

                self.path.append("RH090")#add rotation
                await websocket.send(self.path[0])
                self.log_message(self.path[0])
                next = await websocket.recv()
                if next == "next":
                    self.path.remove(self.path[0])

                if self.station.robot._coordinate[1] < self.station.world._height - 215:
                    self.path.append("DO060")
                    await websocket.send(self.path[0])
                    self.log_message(self.path[0])
                    next = await websocket.recv()
                    if next == "next":
                        self.path.remove(self.path[0])


                await websocket.send("fin")
                self.log_message("fin charge-QR")

                self.station.thread_com_state.speak[str].emit("Decode QR")

                QR = await websocket.recv()

                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame, self.station.world._tableZone)  # redetec robot
                shape = self.station.world._shapeZone._trueCenter
                corectif = self.adjustement(shape)
                self.log_message(QR)
                self.station.thread_com_piece.speak[str].emit(QR)
                await self.send_path(websocket, corectif)#fonction zone piece
                await self.addRotation(shape, websocket)
                await websocket.send("fin")
                self.log_message("fin QR-piece")

                self.station.thread_com_state.speak[str].emit("Recherche de piece")
                piece = await websocket.recv()
                # self.station.vision._visionController.detectRobotAndGetAngleAruco(self.station.camera_monde.frame,self.station.world._tableZone)  # redetec robot

                print("Where do we go :")
                print("points",self.station.world._targetZone._points,QR[-1])
                shape = self.station.world._targetZone._points[int(QR[-1])]
                corectif = self.adjustement(shape)
                print(corectif)
                await self.send_path(websocket, corectif)#fonction target zone
                await self.addRotation(shape, websocket)
                await websocket.send("fin")
                self.log_message("fin piece-drop")

                self.station.thread_com_state.speak[str].emit("Depo de la piece")
                drop = await websocket.recv()
                #self.station.vision._visionController.detectRobotAndGetAngleAruco(
                    #self.station.camera_monde.frame,self.station.world._tableZone)  # redetec robot
                self.log_message(drop)
                await self.send_path(websocket, (54*self.station.world._ratioPixelCm, 54*self.station.world._ratioPixelCm))#fonction depar zone
                await websocket.send("reboot")
                self.log_message("roboot")
                self.station.thread_com_state.speak[str].emit("Arrete")
                self.station.close_timer()

                #self.station.thread_com_volt.speak[str].emit("44")
                #self.station.thread_com_piece.speak[str].emit("blue triangle")
                #self.station.thread_com_pos.speak[str].emit("i:90:076")
                #self.station.thread_com_state.speak[str].emit("progress")
                #self.station.thread_com_image.speak[np.ndarray].emit(np.zeros((400, 200, 3), dtype=np.uint8))

    async def AddMove(self, websocket, move):
        for i in move:
            self.path.append(i)
        while self.path:
            self.calibration()
            sleep(2)
            await websocket.send(self.path[0])
            self.log_message(self.path[0])
            next = await websocket.recv()
            if next == "next":
                self.path.remove(self.path[0])


    async def send_path(self, websocket, destination):
        self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, destination)
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
            datetime.datetime.now()
            datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)
            time = str(datetime.datetime.now())

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


    def adjustement(self, shape):
        sx = shape[0]
        sy = shape[1]
        adjustementX = 0
        adjustementY = 0
        correctif_recul = 120
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
                'ws://'+self.adresse+':4321', ping_interval=70, ping_timeout=10, close_timeout=45) as websocket:#10.240.104.107  192.168.1.38
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

