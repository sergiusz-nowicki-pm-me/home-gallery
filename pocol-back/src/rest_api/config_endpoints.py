from pocol_core.config import BranchExists, BranchNotExists, BranchPathNotExists
from pocol_core.pocol import Pocol
from flask import request

def prepare(app):
    
    @app.route("/config/get-branches")
    def config_get_branches():
        return {"status": "ok", "data": Pocol().getConfig().getBranches()}
    
    
    @app.route("/config/add-branch")
    def config_add_branch():
        path = request.args.get('path', default="?", type=str)
        try:
            return {"status": "ok", "data": Pocol().getConfig().addBranch(path)}
        except BranchExists:
            return {"status": "error", "description": "Branch allready exists"}
        except BranchPathNotExists:
            return {"status": "error", "description": "Branch path not exists"}
            
            
    @app.route("/config/remove-branch")
    def config_remove_branch():
        path = request.args.get('path', default="?", type=str)
        try:
            return {"status": "ok", "data": Pocol().getConfig().removeBranch(path)}
        except BranchNotExists:
            return {"status": "error", "description": "Branch not exists"}
