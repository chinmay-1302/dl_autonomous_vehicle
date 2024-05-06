import asyncio
import websockets

# RASPBERRY_PI_IP = '192.168.1.25'
# RASPBERRY_PI_IP = '10.23.16.71'
RASPBERRY_PI_IP = "ws://192.168.1.46:8765"

async def send_message():
    async with websockets.connect(RASPBERRY_PI_IP) as websocket:
        while True:
            message = input("Enter your message: ")
            print("Sending message:", message)
            await websocket.send(message)
            response = await websocket.recv()
            print("Received response:", response)

asyncio.get_event_loop().run_until_complete(send_message())