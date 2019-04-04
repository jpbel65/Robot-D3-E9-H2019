import asyncio
import websockets
import socket
from time import sleep


async def hello(websocket, path):
    name = await websocket.recv()
    if name == "go":
        await websocket.send("depart")
        while True:
            pos = await websocket.recv()
            print(pos)
            await websocket.send("next")

        
def Connection_Routeur():
    try:
        host = socket.gethostbyname('192.168.1.1')
        s = socket.create_connection((host,80),2)
        return True
    except :
        pass
    return False


start_server = websockets.serve(hello, 'localhost', 8765, ping_interval=70, ping_timeout=10)

#connection = False
#while(connection == False) :
   # connection = Connection_Routeur()

print("ready")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
