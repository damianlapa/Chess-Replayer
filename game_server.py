import asyncio
import datetime
import random
import json
import websockets

all_moves = []

try:
    async def rectangles(websocket, path):
        while True:
            move = await websocket.recv()
            print('Data received:', move)
            if move != 'ready':
                all_moves.append(json.loads(move))

            json.dumps(all_moves)
            await websocket.send(json.dumps(all_moves))
            await asyncio.sleep(random.random() * 3)

            print('Data sent!')


    start_server = websockets.serve(rectangles, "0.0.0.0", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except websockets.ConnectionClosedOK:
    pass
