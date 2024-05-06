import asyncio
import websockets


# RASPBERRY_PI_IP = "192.168.1.25"
# RASPBERRY_PI_IP = "10.23.16.71"
RASPBERRY_PI_IP = "192.168.1.44"
async def echo(websocket, path):
    async for message in websocket:
        print("Received message:", message)
        await websocket.send(message)

start_server = websockets.serve(echo, RASPBERRY_PI_IP, 8766)  # Change port number to 8766 or any other available port

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()