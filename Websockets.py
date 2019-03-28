import asyncio
import websockets
import socket
from time import sleep


async def hello(websocket, path):
    name = await websocket.recv()
    if name == "go":
        sleep(30)
        print(websockets.WebSocketClientProtocol.is_client)
        sleep(30)
        await websocket.send("ok, je vais ou")
        pos = await websocket.recv()
        print(pos)

        
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
