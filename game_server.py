import asyncio
import datetime
import random
import json
import websockets

all_moves = []

try:
    async def data_tracker(websocket, path):
        move = await websocket.recv()
        if move != 'ready':
            all_moves.append(json.loads(move))
        json.dumps(all_moves)
        await websocket.send(json.dumps(all_moves))
        # await asyncio.sleep(random.random() * 3)


    start_server = websockets.serve(data_tracker, "0.0.0.0", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

except websockets.exceptions.ConnectionClosedOK:
    pass
