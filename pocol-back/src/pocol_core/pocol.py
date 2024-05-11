from pocol_core.catalogue import Catalogue
from pocol_core.config import Config
from pocol_core.gallery import Gallery

pocolObj = None

def Pocol():
    global pocolObj
    if pocolObj == None:
        pocolObj = PocolImpl()
    return pocolObj

class PocolImpl:
    def __init__(self):
        self.config = Config()
        self.gallery = Gallery(self.config)
        self.config.load()
        self.catalogue = Catalogue(self.config.getCatalogueFileName())
    
    def getConfig(self):
        return self.config
    
    def getGallery(self):
        return self.gallery
    
    def getCatalogue(self):
        return self.catalogue