
class FileReader:
    """
    Open and read file. Return string with data
    """
    def __init__(self, path):
        """
        Open file from path
        """
        self._path = path
    
    
    def read(self):
        
        data = str()
        try:
            with open(self._path, 'r') as file:
                data = file.read()
        except FileNotFoundError:
            pass
                        
        return data
        

        