import asyncio
from collections import defaultdict

def process_data(data):
    if "put" in data:
        quere = data.lstrip('put ').rstrip('\n')
        quere = quere.split()
        dict[quere[0]].append(float(quere[1]),int(quere[2]))
    return 

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())

def run_server(host,port):
    
    dict = defaultdict(list)
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()