from pocol_core.catalogue import Catalogue
from pocol_core.config import Config
from pocol_core.gallery import Gallery

class Pocol:
    def __init__(self):
        self.config = Config()
        self.gallery = Gallery(self.config)
        self.catalogue = Catalogue(self.config)
        self.config.load()
        
    
    def getConfig(self):
        return self.config
    
    
    def getGallery(self):
        return self.gallery
    
    
    def getCatalogue(self):
        return self.catalogue