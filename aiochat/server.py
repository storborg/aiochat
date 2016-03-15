import sys
import time
import asyncio

import websockets
from websockets.exceptions import ConnectionClosed

from . import model


class ChatServer:
    def __init__(self):
        self.connected = {}

    async def broadcast(self, origin, msg):
        print('ALL > %s' % msg)
        for ws in self.connected:
            if origin != ws:
                await ws.send('%s: %s' % (self.connected[origin], msg))

    async def clock(self):
        # push a message every 5 seconds
        await asyncio.sleep(5)
        return 'The time is ' + time.strftime('%H:%M:%S', time.localtime())

    async def command(self, origin, msg):
        sp = msg.strip().split(None, 1)
        if len(sp) > 1:
            cmd, arg = sp
        else:
            cmd = sp[0]
        assert cmd.startswith('/')
        cmd = cmd[1:]
        if cmd == 'nick':
            self.connected[origin] = arg
            await origin.send('** You are now known as %s **' % arg)
        else:
            await origin.send('** Unknown command. **')

    async def handler(self, websock, path):
        loop = asyncio.get_event_loop()

        addr = websock.remote_address[0]
        self.connected[websock] = name = 'Anonymous %d' % id(websock)
        print('New connection from %s, known as %s' % (addr, name))

        try:
            await websock.send('** You are known as %s **' % name)
            while True:
                listener_task = asyncio.ensure_future(websock.recv())
                clock_task = asyncio.ensure_future(self.clock())
                done, pending = await asyncio.wait(
                    [listener_task, clock_task],
                    return_when=asyncio.FIRST_COMPLETED)

                if listener_task in done:
                    msg = listener_task.result()
                    msg = msg.strip()
                    print('%s < %s' % (addr, msg))
                    if msg.startswith('/'):
                        await self.command(websock, msg)
                    else:
                        name = self.connected[websock]
                        loop.run_in_executor(None,
                                             model.record_message,
                                             addr, name, msg)
                        await self.broadcast(websock, msg)
                        print('%s > ** sent message **' % addr)
                        await websock.send('** sent message **')
                else:
                    listener_task.cancel()

                if clock_task in done:
                    msg = clock_task.result()
                    print('%s > %s' % (addr, msg))
                    await websock.send('Server: ' + msg)
                else:
                    clock_task.cancel()

        except ConnectionClosed:
            print('Disconnected')
        finally:
            del self.connected[websock]


def main(args=sys.argv):
    if len(args) < 2:
        print('usage: %s <port>' % args[0])
    else:
        port = int(args[1])
        chat = ChatServer()
        start_server = websockets.serve(chat.handler, 'localhost', port)
        model.init('sqlite:///messages.db')
        print("Listening on port %d..." % port)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        loop.run_forever()
