#!/usr/bin/env python

import asyncio
import websockets
import json
from random import randint


async def send_json(json_message: dict) -> None:
    uri = "ws://localhost:8765"

    # Make string representation
    json_message['data'] = [randint(0, 50) for _ in range(randint(25,100))]
    json_message = json.dumps(json_message)

    async with websockets.connect(uri) as websocket:

        await websocket.send(json_message)
        print(f"> message sent")

        response = await websocket.recv()
        print(f"< {response}")

if __name__ == "__main__":
    import sys

    _id = sys.argv[1]
    
    json_data = {
        'id': _id,
        'data': None
    }
    asyncio.get_event_loop().run_until_complete(send_json(json_data))