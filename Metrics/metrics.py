import socket
import time

class ClientError(Exception):
    pass

class Client:
    """
    Client for put and get metrics
    """
    
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout

    def put(self, key, value, timestamp=None):
        with socket.create_connection((self._host, self._port),self._timeout) as sock:
            try:    
                if timestamp is None:
                    timestamp = int(time.time())
                sock.sendall(("put {} {} {}\n".format(key, value, timestamp)).encode("utf8"))
                ansver = sock.recv(1024).decode("utf8")
            except socket.error:
                raise ClientError
            if "ok\n\n" not in ansver:
                raise ClientError


    def get(self, key):
        pass
        return None