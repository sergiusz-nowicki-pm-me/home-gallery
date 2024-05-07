from pocol_core.catalogue import CategoryAlreadyExists
from pocol_core.pocol import Pocol
from flask import request

def prepare(app):
    
    @app.route("/catalogue/category/create")
    def category_create():
        if "name" not in request.args:
            return {"status": "error", "description": "Category name not found"}
        name = request.args.get("name", type=str)
        
        try:
            Pocol().getCatalogue().addCategory(name)
            return {"status": "ok"}
        except CategoryAlreadyExists:
            return {"status": "error", "description": "Category already exists"}
        
        
    @app.route("/catalogue/category/add-parent")
    def category_add_parent():
        if "name" not in request.args:
            return {"status": "error", "description": "Category name not found"}
        name = request.args.get("name", type=str)
        
        if "parent-name" not in request.args:
            return {"status": "error", "description": "Parent name not found"}
        parent_name = request.args.get("parent-name", type=str)
        
        try:
            Pocol().getCatalogue().getCategory(name).addParent(parent_name)
            return {"status": "ok"}
        except:
            return {"status": "error", "description": ""}
            
    @app.route("/catalogue/category/list-all")
    def category_list_all():
        return [c.getName() for c in Pocol().getCatalogue().getCategories()]

    @app.route("/catalogue/category/list-subcategories")
    def category_list_subcategories():
        if "name" not in request.args:
            return {"status": "error", "description": "Category name not found"}
        name = request.args.get("name", type=str)

        max_lvl = 1
        if "max-lvl" in request.args:
            max_lvl = request.args.get("max-lvl", type=int)

        return [c.getName() for c in Pocol().getCatalogue().getCategory(name).getSubcategories(max_lvl=max_lvl)]
