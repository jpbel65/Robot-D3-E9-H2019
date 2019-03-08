import asyncio
import websockets
import socket

async def hello(websocket, path):
    name = await websocket.recv()
    if name == "go":
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

connection = False
while(connection == False) :
    connection = Connection_Routeur()
    
start_server = websockets.serve(hello, "192.168.1.38", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
