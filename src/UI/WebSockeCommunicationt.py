import keyboard
import threading
import asyncio
import websockets
from time import sleep


class WebSocket:
    logResult = ""
    path = []

    def __init__(self, log_window):
        self.textArea = log_window

    async def start_communication_web(self):
        async with websockets.connect(
                'ws://localhost:8765') as websocket:
            go = "go"
            await websocket.send(go)
            self.log_message(go)
            #self.path.append("l,l,u")#cree a thread qui fait le pathfinding et push les chemin dans une list producteur
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

    def thread_start_comm_web(self):
        t2 = threading.Thread(target=self.async_run_comm_web)
        t2.start()

    def async_run_comm_web(self):
        asyncio.run(self.start_communication_web())

    def log_message(self, message):
        self.logResult += message + "\n"
        self.textArea.value = self.logResult
