import keyboard
import threading
import asyncio
import websockets
from time import sleep
import numpy as np
import signal


class WebSocket(websockets.WebSocketCommonProtocol):
    logResult = ''
    path = []

    def __init__(self, log_window, station):
        self.textArea = log_window
        self.station = station
        super().__init__()
        super().ping_interval = 10

    async def start_communication_web(self):
        async with websockets.connect(
                'ws://10.248.95.160:8765') as websocket:#10.240.86.202:8765
            go = "go"
            await websocket.send(go)
            self.log_message(go)
            self.path.append("DS001")
            self.path.append("DN001")#cree a thread qui fait le pathfinding et push les chemin dans une list producteur
            #self.station.path_finding.thread_start_pathfinding(123, 32)
            ready = await websocket.recv()
            if ready == "depart":
                self.log_message(ready)
                print("< {ready}")
                await self.send_path(websocket)#fonction
                await websocket.send("fin")
                self.log_message("fin start-charge")
                self.station.thread_com_state.speak[str].emit("Charge")
                tension = await websocket.recv()
                self.log_message(tension)
                self.station.thread_com_volt.speak[str].emit(tension)
                await websocket.send("ok")
                courant = await websocket.recv()
                self.log_message(courant)
                self.station.thread_com_courant.speak[str].emit(courant)
                self.path.append("DE003")
                self.path.append("DO003")
                await self.send_path(websocket)#fonction
                await websocket.send("fin")
                self.log_message("fin charge-QR")
                self.station.thread_com_state.speak[str].emit("Decode QR")
                QR = await websocket.recv()
                self.log_message(QR)
                self.station.thread_com_piece.speak[str].emit(QR)
                self.path.append("DN006")
                self.path.append("DS006")
                await self.send_path(websocket)#fonction
                await websocket.send("fin")
                self.log_message("fin QR-piece")
                self.station.thread_com_state.speak[str].emit("Recherche de piece")
                piece = await websocket.recv()
                self.log_message(piece)
                self.path.append("DO005")
                self.path.append("DE005")
                await self.send_path(websocket)#fonction
                await websocket.send("fin")
                self.log_message("fin piece-drop")
                self.station.thread_com_state.speak[str].emit("Depo de la piece")
                drop = await websocket.recv()
                self.log_message(drop)
                self.path.append("DS005")
                self.path.append("DN005")
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


