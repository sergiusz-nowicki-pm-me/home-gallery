from pocol_core.pocol import Pocol
from flask import request

def prepare(app):
    
    @app.route("/query/get-matching-image-sets")
    def get_matching_image_sets():
        name = request.args.get("name", default="*", type=str)
        return {"status": "ok", "data": Pocol().getGallery().getMatchingSets(name)}
