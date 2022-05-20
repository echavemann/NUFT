#!/usr/bin/env python
import asyncio
import json
import logging
import time
import os
import websockets
from concurrent.futures import ProcessPoolExecutor
from functools import reduce

logging.basicConfig(level=logging.INFO,
                    format='PID %(process)-10d %(asctime)s %(message)s'
                    )

task_executer = ProcessPoolExecutor(max_workers=3)

def data_processor(raw_message):
    pid = os.getpid()

    message = json.loads(raw_message)
    print(f'PID {pid:<10} ID {message["id"]} message deserialized')

    message_data = message['data']
    result = reduce(lambda a,b: int(a)+int(b), message_data)

    # Sleeping just for visualizing things in the logs sake
    time.sleep(1.0)

    print(f'PID {pid:<10} Result {result}')

    result_message = {
        'id': message['id'],
        'result': result
    }

    return result_message


async def producer(websocket, path, message):
    log = logging.getLogger('producer')
    log.info('Received processed message')
    log.info(f'Sending {message["id"]}')

    serialized_message = json.dumps(message)

    await websocket.send(serialized_message)


async def listener(websocket, path):
    tasks =  []

    log = logging.getLogger('listener')
    loop = asyncio.get_running_loop()
    async for json_message in websocket:

        tasks.append(
            loop.run_in_executor(task_executer, data_processor, json_message)
        )
        for task in asyncio.as_completed(tasks):
            _message = await task
            loop.create_task(producer(websocket, path, _message))

try:
    start_server = websockets.serve(listener, "localhost", 8765)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(start_server)
    loop.run_forever()
except Exception as e:
    print(f'Caught exception {e}')
    pass
finally:
    loop.close()