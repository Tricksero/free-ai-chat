import asyncio
import websockets
import json
import logging
import logging

async def connect_to_channel():
    async with websockets.connect("ws://localhost:8000/ws/api/new/", origin="http://localhost/") as websocket:
        # Send a message to the channel to authenticate and join the room
        await websocket.send(json.dumps({"message": "message from python"}))

        # Receive messages from the channel
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received message: {data['message']}")

asyncio.run(connect_to_channel())