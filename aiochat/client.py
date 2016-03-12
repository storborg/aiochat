import sys
import asyncio
import websockets


def stdin_handler(q):
    asyncio.async(q.put(sys.stdin.readline()))


async def client(server, q):
    async with websockets.connect('ws://%s' % server) as websock:
        while True:
            printer_task = asyncio.ensure_future(websock.recv())
            sender_task = asyncio.ensure_future(q.get())
            done, pending = await asyncio.wait(
                [printer_task, sender_task],
                return_when=asyncio.FIRST_COMPLETED)

            if printer_task in done:
                msg = printer_task.result()
                print(msg)
            else:
                printer_task.cancel()

            if sender_task in done:
                msg = sender_task.result()
                await websock.send(msg)
            else:
                sender_task.cancel()


def main(args=sys.argv):
    if len(args) < 2:
        print("usage: %s <server hostname>" % args[0])
    else:
        host = args[1]
        q = asyncio.Queue()
        loop = asyncio.get_event_loop()
        loop.add_reader(sys.stdin, stdin_handler, q)
        loop.run_until_complete(client(host, q))
