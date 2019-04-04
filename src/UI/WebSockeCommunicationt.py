import keyboard
import threading
import asyncio
import websockets
from time import sleep
import numpy as np
import signal


class WebSocket(websockets.WebSocketCommonProtocol):
    logResult = ''
    #path = []

    def __init__(self, log_window, station):
        super(WebSocket, self).__init__()
        self.textArea = log_window
        self.station = station
        print(self.ping_interval)
        print(self.ping_timeout)
        self.path = []

    def testOffline(self, bool):
        if bool:
            print("Path found : ")
            self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate,
                                                               (self.station.world._width-300 + self.station.world._axisX, self.station.world._width/2 + self.station.world._axisY))

            for obstacle in self.station.world._obstacles:
                print(obstacle._coordinate)

            print(self.station.world._shapeZone._center)
            print(self.station.robot._angle)
            print(self.station.world._targetZone.center)

    async def start_communication_web(self):
        print("start comm")

        self.testOffline(False)

        async with websockets.connect(
                'ws://localhost:8765', ping_interval=70, ping_timeout=10) as websocket:#10.240.104.107
            print("in websocket")
            go = "go"
            await websocket.send(go)
            self.log_message(go)

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

            self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (119 + self.station.world._axisX, self.station.world._height-100 + self.station.world._axisY - 103))
            #self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (
            #        119 + self.station.world._axisX, self.station.world._height - 100 + self.station.world._axisY + 3030))
            print(self.path)
            ready = await websocket.recv()
            print(ready)
            if ready == "depart":
                self.log_message(ready)
                print("< {ready}")
                await self.send_path(websocket)#fonction
                await websocket.send("fin")
                self.log_message("fin start-charge")

                self.station.thread_com_state.speak[str].emit("Charge")
                tension = await websocket.recv()
                self.log_message(tension)
                self.station.vision._visionController.detectRobotAndGetAngle(self.station.camera_monde.frame)#redetec robot
                self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (self.station.world._width-200 + self.station.world._axisX,
                                                                                                    self.station.world._height/2 + self.station.world._axisY))#vers qr
                self.station.thread_com_volt.speak[str].emit(tension)
                await websocket.send("ok")
                courant = await websocket.recv()
                self.log_message(courant)
                self.station.thread_com_courant.speak[str].emit(courant)
                await self.send_path(websocket)#fonction
                self.path.append("RH090")#add reotation
                await websocket.send(self.path[0])
                self.log_message(self.path[0])
                next = await websocket.recv()
                if next == "next":
                    self.path.remove(self.path[0])
                    self.log_message(next)
                await websocket.send("fin")
                self.log_message("fin charge-QR")

                self.station.thread_com_state.speak[str].emit("Decode QR")
                self.station.vision._visionController.detectRobotAndGetAngle(self.station.camera_monde.frame)  # redetec robot
                shape = self.station.world._shapeZone._center
                corectif = self.adjustement(shape)
                self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (shape[0]+corectif[0], shape[1]+corectif[1]))# vers pick up - a add
                QR = await websocket.recv()
                self.log_message(QR)
                self.station.thread_com_piece.speak[str].emit(QR)
                await self.send_path(websocket)#fonction
                await self.addRotation(shape, websocket)
                await websocket.send("fin")
                self.log_message("fin QR-piece")

                self.station.thread_com_state.speak[str].emit("Recherche de piece")
                piece = await websocket.recv()
                self.station.vision._visionController.detectRobotAndGetAngle(
                    self.station.camera_monde.frame)  # redetec robot
                shape = self.station.world._targetZoneZone._center
                corectif = self.adjustement(shape)
                self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (
                shape[0] + corectif[0], shape[1] + corectif[1]))  # vers pick up - a add
                self.log_message(piece)
                await self.send_path(websocket)#fonction
                await self.addRotation(shape, websocket)
                await websocket.send("fin")
                self.log_message("fin piece-drop")

                self.station.thread_com_state.speak[str].emit("Depo de la piece")
                drop = await websocket.recv()
                self.station.vision._visionController.detectRobotAndGetAngle(
                    self.station.camera_monde.frame)  # redetec robot
                self.station.path_finding.thread_start_pathfinding(self.station.robot._coordinate, (292 + self.station.world._axisX, 324 + self.station.world._axisY))  # vers pick up - a add
                self.log_message(drop)
                await self.send_path(websocket)#fonction
                await websocket.send("reboot")
                self.log_message("roboot")
                self.station.thread_com_state.speak[str].emit("Arrete")

                #self.station.thread_com_volt.speak[str].emit("44")
                #self.station.thread_com_piece.speak[str].emit("blue triangle")
                #self.station.thread_com_pos.speak[str].emit("i:90:076")
                #self.station.thread_com_state.speak[str].emit("progress")
                #self.station.thread_com_image.speak[np.ndarray].emit(np.zeros((400, 200, 3), dtype=np.uint8))

    async def send_path(self, websocket):
        await self.calibration(websocket)
        self.station.thread_com_state.speak[str].emit("Mouvement")
        while not self.path:
            self.log_message("WS empty")
            sleep(2)
        while self.path:
            await websocket.send(self.path[0])
            self.log_message(self.path[0])
            next = await websocket.recv()
            if next == "next":
                self.path.remove(self.path[0])
                self.log_message(next)

    async def calibration(self, websocket):
        self.station.thread_com_state.speak[str].emit("Calibration")
        angle = int(self.station.robot._angle) + 1  # +1 correctif angle
        side = "H"
        if angle < 0:
            side = "A"
            angle = abs(angle)
        angle = str(angle)
        while len(angle) is not 3:
            angle = "0" + angle
        self.path.append("R" + side + angle)  # rota angle depart
        await websocket.send(self.path[0])
        self.log_message(self.path[0])
        next = await websocket.recv()
        if next == "next":
            self.path.remove(self.path[0])
            self.log_message(next)

    async def addRotation(self, obj, websocket):
        if obj[1] > self.station.world._height/2:
            self.path.append("RH090")
        elif obj[1] < self.station.world._height/2:
            self.path.append("RA090")
        await websocket.send(self.path[0])
        self.log_message(self.path[0])
        next = await websocket.recv()
        if next == "next":
            self.path.remove(self.path[0])
            self.log_message(next)

    def adjustement(self, shape):
        adjustementX = 0
        adjustementY = 0
        if shape[1] > self.station.world._height / 2:
            adjustementY = 146
        elif shape[1] < self.station.world._height / 2:
            adjustementY = -146
        if shape[0] > self.station.world._width - 108:
            adjustementX = -146
        return (adjustementX, adjustementY)

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


