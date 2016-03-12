import sys
import time
import asyncio

import websockets
from websockets.exceptions import ConnectionClosed


connected = set()


async def broadcast(origin, msg):
    for ws in connected:
        if ws != origin:
            await ws.send('%s' % msg)


async def clock():
    # push a message every 5 seconds
    await asyncio.sleep(5)
    return 'The time is ' + time.strftime('%H:%M:%S', time.localtime())


async def handler(websock, path):
    global connected
    print('new connection')
    connected.add(websock)
    try:
        while True:
            listener_task = asyncio.ensure_future(websock.recv())
            clock_task = asyncio.ensure_future(clock())
            done, pending = await asyncio.wait(
                [listener_task, clock_task],
                return_when=asyncio.FIRST_COMPLETED)

            if listener_task in done:
                msg = listener_task.result()
                msg = msg.strip()
                print('< %r' % msg)
                await broadcast(websock, msg)
                await websock.send('** sent message **')
            else:
                listener_task.cancel()

            if clock_task in done:
                msg = clock_task.result()
                print('> %r' % msg)
                await broadcast(None, msg)
            else:
                clock_task.cancel()

    except ConnectionClosed:
        print('disconnected')
    finally:
        connected.remove(websock)


def main(args=sys.argv):
    if len(args) < 2:
        print('usage: %s <port>' % args[0])
    else:
        port = int(args[1])
        start_server = websockets.serve(handler, 'localhost', port)
        print("Listening on port %d" % port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
