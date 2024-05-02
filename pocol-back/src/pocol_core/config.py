import os
import json
from flask import request

CONFIG_FILE_NAME = 'pocol.conf'
EVT_BRANCH_ADD = "BRANCH ADD"

class BranchExists(Exception): pass
class BranchNotExists(Exception): pass
class BranchPathNotExists(Exception): pass

class Config:
    
    def __init__(self):
        self.root_change_listeners = []
        self.branches = []
        
        
    def load(self):
        if not os.path.exists(CONFIG_FILE_NAME):
            self.__dump__()
        self.__load__()


    def __dump__(self):
        with open(CONFIG_FILE_NAME, 'w') as f:
            json.dump({"branches": self.branches}, f, sort_keys=True)
        
    
    def __load__(self):
        with open(CONFIG_FILE_NAME, 'r') as f:
            config = json.load(f)
            if "branches" in config:
                self.branches = config["branches"]
                for b in self.branches:
                    self.__fireBranchChange__(EVT_BRANCH_ADD, path=b)
                
                
    def addBranchChangeListener(self, listener):
        if not callable(listener):
            raise Exception("Branch change listener must be callable")
        
        if listener not in self.root_change_listeners:
            self.root_change_listeners.append(listener)
            
            
    def __fireBranchChange__(self, evt_name, **kwargs):
        for l in self.root_change_listeners:
            l(evt_name, **kwargs)
        

    def getBranches(self):
        return self.branches
    
    
    def addBranch(self, path):
        if path in self.branches:
            raise BranchExists()
        
        if not os.path.exists(path):
            raise BranchPathNotExists()
        
        if os.path.isfile(path):
            raise BranchPathNotExists()
            
        self.branches.append(path)
        self.__dump__()
        self.__fireBranchChange__(EVT_BRANCH_ADD, path=path)
        return self.branches

    
    def removeBranch(self, path):
        if not path in self.branches:
            raise BranchNotExists()
        self.branches.remove(path)
        self.__dump__()
        self.__fireBranchChange__("BRANCH REMOVE", path=path)
        return self.branches