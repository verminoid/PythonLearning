import socket
import time

class ClientError(Exception):
    pass

def ParcerGet(data):
    parced_dict = dict()
    for line in data.split("\n"):
        if line == "ok":
            continue
        elif line is None:
            break
        str = line.split(" ")
        temp = parced_dict.get(str[0])
        if temp in None:
            parced_dict.update(str[0],tuple(int(str[2]),float(str[1])))
        else:
            parced_dict[str[0]] = temp.append(tuple(int(str[2]),float(str[1])))
    for item in parced_dict:
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
        # TODO создать соединение здесь
                # создать удаление с закрытием сокета

    def put(self, key, value, timestamp=None):
        with socket.create_connection((self._host, self._port),self._timeout) as sock:
            try:    
                if timestamp is None:
                    timestamp = int(time.time())
                sock.sendall(("put {} {} {}\n".format(key, value, timestamp)).encode("utf8"))
                ansver = sock.recv(1024).decode("utf8")
                if "ok\n\n" not in ansver:
                    raise ClientError
            except socket.error:
                raise ClientError
            


    def get(self, key):
        
        with socket.create_connection((self._host, self._port),self._timeout) as sock:
            sock.sendall("get {}\n".format(key).encode("utf8"))
            ansver = sock.recv(1024).decode("utf8")
            if "ok\n" in ansver:
                return ParcerGet(ansver)
            else:
                raise ClientError
        
