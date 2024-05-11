from pocol_core.pocol import Pocol
from flask import request

def prepare(app):
    @app.route("/query/get-matching-image-sets")
    def get_matching_image_sets():
        name = request.args.get("name", default="*", type=str)
        return {"status": "ok", "data": Pocol().getGallery().getMatchingSets(name)}

    @app.route("/query/get-image-set/<id>")
    def get_image_set(id):
        set = Pocol().getGallery().getImageSet(id)
        if set != None:
            return {"status": "ok", "data": {"id": set.getUuid(), "images": set.getFiles()}}
        else:
            return {"status": "error", "description": "Image set not found"}