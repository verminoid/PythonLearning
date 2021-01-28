import socket
import time
from collections import defaultdict

class ClientError(Exception):
    pass

def ParcerGet(data):
    if data == "ok\n\n":
        return dict()
    if data == 'error\nwrong command\n\n':
        raise ClientError()
    items = data.lstrip('ok\n').rstrip('\n\n')
    items = [x.split() for x in items.split('\n')]
    parced_dict = defaultdict(list)
    for key, metric, timestamp in items:
        parced_dict[key].append((int(timestamp), float(metric)))
    for item in parced_dict.values():
        item.sort()
    return parced_dict

    

class Client:
    """
    Client for put and get metrics
    """
    
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        self.sock = socket.create_connection((self._host, self._port),self._timeout)

    def __del__(self):
        self.sock.close()

    def put(self, key, value, timestamp=None):
        try:    
            if timestamp is None:
                timestamp = int(time.time())
            self.sock.sendall(("put {} {} {}\n".format(key, value, timestamp)).encode("utf8"))
            ansver = self.sock.recv(1024).decode("utf8")
            if "ok\n\n" not in ansver:
                raise ClientError()
        except socket.error:
            raise ClientError()
            


    def get(self, key):
        
        self.sock.sendall("get {}\n".format(key).encode("utf8"))
        ansver = self.sock.recv(1024).decode("utf8")
        return ParcerGet(ansver)
        
        
