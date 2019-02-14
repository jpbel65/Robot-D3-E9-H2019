import asyncio
import websockets


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")
    if name == "go":
        await websocket.send("ok, je vais ou")
        pos = await websocket.recv()
        print(pos)


async def pong(websocket, path):
    ping = await websocket.recv()
    if ping == "ping":
        await websocket.send("pong")

start_server = websockets.serve(hello, 'localhost', 8765)
start_server_pong = websockets.serve(pong, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
