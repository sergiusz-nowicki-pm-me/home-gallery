import os
import json
import uuid

from PIL import Image


METADATA_FILE_NAME = 'zzz.metadata'


class ImageSet:
    def __init__(self, path):
        print("Image set", path)
        self.path = path
        self.name = os.path.basename(self.path)
        self.metadata = {}
        self.__loadMetadata__()
        
        
    def __loadMetadata__(self):
        metadata_file = os.path.join(self.path, METADATA_FILE_NAME)
        if not os.path.exists(metadata_file):
            files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
            files_dict = {}
            index = 0
            for f in files:
                try:
                    Image.open(os.path.join(self.path, f))
                    files_dict[index] = f
                    index += 1
                except:
                    pass
            self.metadata = {"uuid": uuid.uuid4().hex, "files": files_dict}
            self.__dumpMetadata__()
        else:
            with open(metadata_file, "r") as f:
                self.metadata = json.load(f)
            
            
    def __dumpMetadata__(self):
        metadata_file = os.path.join(self.path, METADATA_FILE_NAME)
        with open(metadata_file, "w") as f:
            json.dump(self.metadata, f)
    
    
    def getName(self):
        return self.name
    
    
    def getUuid(self):
        return self.metadata["uuid"]