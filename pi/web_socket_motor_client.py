import asyncio
import websockets
import keyboard

# 1 = forward
# 2 = reverse
# 3 = left
# 4 = right
to_ard = ["1", "2", "3", "4"]
keys = ["w", "s", "a", "d"]

async def send_message():
    async with websockets.connect("ws://192.168.1.47:8766") as websocket:
        while True:
            # message = input("Write Message: ")
            if keyboard.is_pressed(keys[0]):
                print("Sending message:", to_ard[0])
                await websocket.send(to_ard[0])
                response = await websocket.recv()
                print("Received response:", response)
            elif keyboard.is_pressed(keys[1]):
                print("Sending message:", to_ard[1])
                await websocket.send(to_ard[1])
                response = await websocket.recv()
                print("Received response:", response)
            elif keyboard.is_pressed(keys[2]):
                print("Sending message:", to_ard[2])
                await websocket.send(to_ard[2])
                response = await websocket.recv()
                print("Received response:", response)
            elif keyboard.is_pressed(keys[3]):
                print("Sending message:", to_ard[3])
                await websocket.send(to_ard[3])
                response = await websocket.recv()
                print("Received response:", response)
asyncio.get_event_loop().run_until_complete(send_message())