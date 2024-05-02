import json
import os


CATALOGUE_FILE_NAME = "catalogue.json"

CATEGORIES = "categories"


class CategoryAlreadyExists(Exception): pass
class ParentCategoryNotExists(Exception): pass


class Catalogue:
    def __init__(self, config):
        self.data = {CATEGORIES: {}}
        self.load()
        
        
    def load(self):
        if not os.path.exists(CATALOGUE_FILE_NAME):
            self.__dump__()
        self.__load__()


    def __dump__(self):
        with open(CATALOGUE_FILE_NAME, 'w') as f:
            json.dump(self.data, f, sort_keys=True, indent=2)
        
    
    def __load__(self):
        with open(CATALOGUE_FILE_NAME, 'r') as f:
            self.data = json.load(f)
            
            
    def addCategory(self, name, multiplicity, parent):
        if name in self.data[CATEGORIES]:
            raise CategoryAlreadyExists()
        if parent != None and parent not in self.data[CATEGORIES]:
            raise ParentCategoryNotExists()

        if parent != None:
            self.data[CATEGORIES][name] = {"multiplicity": multiplicity, "parent": parent, "objects": []}
        else:
            self.data[CATEGORIES][name] = {"multiplicity": multiplicity, "objects": []}
        self.__dump__()


    def getCategories(self):
        return self.data[CATEGORIES]
