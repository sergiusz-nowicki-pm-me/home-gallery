from flask import send_file
from pocol_core.pocol import Pocol

def prepare(app):
    @app.route("/image/<gallery_id>/<file_no>")
    def get_image(gallery_id, file_no):
        set = Pocol().getGallery().getImageSet(gallery_id)
        if set != None:
            return send_file(set.getFile(file_no))
        else:
            return {"status": "error", "description": "Image set not found"}
        
    # @app.route("/query/get-image-set/<id>")
    # def get_image_set(id):
    #     set = Pocol().getGallery().getImageSet(id)
    #     if set != None:
    #         return {"status": "ok", "data": {"id": set.getUuid(), "images": set.getFiles()}}
    #     else:
    #         return {"status": "error", "description": "Image set not found"}