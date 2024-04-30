import fnmatch
import os

from pocol_core.image_set import ImageSet


class Branch:
    def __init__(self, path):
        self.path = path
        self.sets = []
        
        print("Branch", path)
        self.__loadMetadata__()
        
    
    def __loadMetadata__(self):
        for root, dirs, files in os.walk(self.path):
            if len(files) > 0:
                self.sets.append(ImageSet(root))


    def getMatchingSets(self, name):
        result = {s.getUuid() : s.getName() for s in self.sets if len(fnmatch.filter([s.getName()], name)) > 0}
        print(result)
        return result