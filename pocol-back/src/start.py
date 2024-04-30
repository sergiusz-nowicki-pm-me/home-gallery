
import logging
from pocol import Pocol





rest_api.config_endpoints.prepare()

# pocol = Pocol("y:\\Референсы\\photo\\!HollyRandall\\")
# pocol.init()
logger = logging.getLogger("main")
ConsoleOutputHandler = logging.StreamHandler()
logger.addHandler(ConsoleOutputHandler)


@app.route("/")
def index():
    return "POCOL-BACK"




    
@app.route("/list-all-galleries")
def list_all_galleries():
    return pocol.list_all_galleries()


@app.route("/gallery/get/<uuid>")
def gallery_get(uuid):
    return pocol.get_gallery(uuid).get_metadata()


@app.route("/image/get/<gallery_uuid>/<uuid>")
def image_get(gallery_uuid, uuid):
    path = pocol.get_gallery(gallery_uuid).get_image_path(uuid)
    return send_file(path)


@app.route("/image/get-thumb/<gallery_uuid>/<uuid>")
def image_get_thumb(gallery_uuid, uuid):
    path = pocol.get_gallery(gallery_uuid).get_image_thumb(uuid)
    return send_file(path)


@app.route("/image/get-first-thumb/<gallery_uuid>")
def image_get_first_thumb(gallery_uuid):
    path = pocol.get_gallery(gallery_uuid).get_firts_thumb_path()
    return send_file(path)


@app.route("/gallery/tag/add/<gallery_uuid>/<type>/<name>")
def gallery_tag_add(gallery_uuid, type, name):
    g = pocol.get_gallery(gallery_uuid)
    return "ok"