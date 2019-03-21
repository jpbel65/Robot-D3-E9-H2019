import keyboard
import threading
import asyncio
import websockets
from time import sleep
import numpy as np
import signal


class WebSocket:
    logResult = ''
    path = []

    def __init__(self, log_window, station):
        self.textArea = log_window
        self.station = station

    async def start_communication_web(self):
        async with websockets.connect(
                'ws://localhost:8765') as websocket:#10.240.86.202:8765
            go = "go"
            await websocket.send(go)
            ret_log = self.log_message(go)
            #self.path.append("l,l,u")#cree a thread qui fait le pathfinding et push les chemin dans une list producteur
            self.station.path_finding.thread_start_pathfinding()
            ready = await websocket.recv()
            if ready == "ok, je vais ou":
                self.log_message(ready)
                print("< {ready}")
                while not self.path:
                    self.log_message("WS empty")
                    if keyboard.is_pressed('q'):
                        self.path.append("l,l,u")
                    sleep(5)
                await websocket.send(self.path[0])
                self.log_message(self.path[0])
                self.station.thread_com_volt.speak[str].emit("44")
                self.station.thread_com_piece.speak[str].emit("blue triangle")
                self.station.thread_com_pos.speak[str].emit("i:90:076")
                self.station.thread_com_state.speak[str].emit("progress")
                self.station.thread_com_image.speak[np.ndarray].emit(np.zeros((400, 200, 3), dtype=np.uint8))

    def thread_start_comm_web(self):
        t2 = threading.Thread(target=self.async_run_comm_web)
        t2.start()
        #t2.join()

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


