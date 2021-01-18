import asyncio
from collections import defaultdict


class ClientServerProtocol(asyncio.Protocol):

    dict = defaultdict(list)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host,port):
    
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

def process_data(data):
    quere = data.split()
    com = quere[0]
    out = ""
    if com not in ("put","get"):
        out = "error\nwrong command\n\n"
    else: 
        out = "ok\n"
    if com == "put":
        dataset = quere[1:]
        key, metric, timestamp = dataset
        ClientServerProtocol.dict[key].append((float(metric),int(timestamp)))
       
    if com == "get":
        if len(quere)>1:
            k = quere[1]
            if k == "*":
                for key, values in ClientServerProtocol.dict.items():
                    for metric, timestamp in values:
                        out += "{} {} {}\n".format(key, metric, timestamp)
            else:
                for (metric, timestamp) in ClientServerProtocol.dict[k]:
                    out += "{} {} {}\n".format(k, metric, timestamp)
    out += "\n"
    
    return out

run_server("localhost", 8888)