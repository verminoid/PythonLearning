import os.path
import tempfile

def write_file(path, data):
    try:
        with open(path, 'w') as file:
            file.write(data)
    except FileNotFoundError:
        pass

def read_file(path):
    data = str()
    try:
        with open(path, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        pass                        
    return data

class File:
    
    def __init__(self, path):
        self._path = path
        self._cur = 0
        self._end = 0
        self._data = []
        if not os.path.exists(self._path):
            write_file(self._path, '')

    def __str__(self):
        return '{}'.format(self._path)

    def __repr__(self):
        return '{}'.format(self._path)

    def __add__(self, obj):
        data = read_file(self._path) + read_file(obj._path)
        storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
        write_file(storage_path, data)
        return File(storage_path)
    
    def read(self):
        return read_file(self._path)

    def write(self, new_data):
        write_file(self._path, new_data)

    #попробовать переделать этот метод

    def __iter__(self):
        with open(self._path, 'r') as f:
            self._data = f.readlines()
            self._end = len(self._data)
        return self

    def __next__(self):
        if self._cur >= self._end:
            self._data.clear()
            raise StopIteration
        result = self._data[self._cur]
        self._cur += 1
        return result

    
    

        
        