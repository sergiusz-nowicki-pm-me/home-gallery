from pocol_core.catalogue import CategoryAlreadyExists
from pocol_core.pocol import Pocol
from flask import request

from .utils import getRequestParam, ParamNotFound

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
        try:
            name = getRequestParam("name", type=str)
            parent_name = getRequestParam("parent-name", type=str)
            Pocol().getCatalogue().getCategory(name).addParent(parent_name)
            return {"status": "ok"}
        except ParamNotFound:
            return {"startus": "error", "description": "Parameter is missing"}
        except:
            return {"status": "error", "description": ""}
            
    @app.route("/catalogue/category/list-all")
    def category_list_all():
        return [c.getName() for c in Pocol().getCatalogue().getCategories()]

    @app.route("/catalogue/category/list-subcategories")
    def category_list_subcategories():
        try:
            name = getRequestParam("name", type=str)
            max_lvl = getRequestParam("max-lvl", default=1, type=int)
            return [c.getName() for c in Pocol().getCatalogue().getCategory(name).getSubcategories(max_lvl=max_lvl)]
        except ParamNotFound:
            return {"startus": "error", "description": "Parameter is missing"}

    @app.route("/catalogue/category/list-parents")
    def category_list_parents():
        try:
            name = getRequestParam("name", type=str)
            return [c.getName() for c in Pocol().getCatalogue().getCategory(name).getAllParents()]
        except ParamNotFound:
            return {"startus": "error", "description": "Parameter is missing"}

    @app.route("/catalogue/object/assign-category")
    def assign_category():
        try:
            object_uuid = getRequestParam("uuid", type=str)
            category_name = getRequestParam("category-name", type=str)
            Pocol().getCatalogue().getCategory(category_name).assign(object_uuid)
        except ParamNotFound:
            return {"startus": "error", "description": "Parameter is missing"}