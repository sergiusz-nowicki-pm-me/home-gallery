from pocol_core.branch import Branch
from pocol_core.config import EVT_BRANCH_ADD


class Gallery:
    def __init__(self, config):
        self.config = config
        self.branches = []
        self.config.addBranchChangeListener(lambda e, **kwargs: self.__configChanged__(e, **kwargs))
        
    def __configChanged__(self, evn_name, **kwargs):
        if evn_name == EVT_BRANCH_ADD:
            if "path" in kwargs:
                path = kwargs["path"]
                self.branches.append(Branch(path))
            else:
                raise Exception("Branch path is not supplied")

    def getMatchingSets(self, name="*"):
        result = {}
        for b in self.branches:
            result.update(b.getMatchingSets(name))
        return result

    def getImageSet(self, id):
        for b in self.branches:
            for s in b.getAllSets():
                if s.getUuid() == id:
                    return s
        return None
