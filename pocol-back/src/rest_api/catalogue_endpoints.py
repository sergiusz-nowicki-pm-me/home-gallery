from pocol_core.catalogue import CategoryAlreadyExists
from pocol_core.pocol import Pocol
from flask import request

def prepare(app):
    
    @app.route("/catalogue/category/create")
    def category_create():
        if "name" not in request.args:
            return {"status": "error", "description": "Category name not found"}
        name = request.args.get("name", type=str)
        
        if "multiplicity" not in request.args:
            return {"status": "error", "description": "Multiplicity not found"}
        multiplicity = request.args.get("multiplicity", type=str)
        
        parent = None
        if "parent" in request.args:
            parent = request.args["parent"]

        try:
            Pocol().getCatalogue().addCategory(name, multiplicity, parent)
            return {"status": "ok"}
        except CategoryAlreadyExists:
            return {"status": "error", "description": "Category already exists"}
            


    @app.route("/catalogue/category/list-all")
    def category_list_all():
        return Pocol().getCatalogue().getCategories()
