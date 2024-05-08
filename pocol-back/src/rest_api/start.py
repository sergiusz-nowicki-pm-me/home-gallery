from flask import Flask, send_file
from flask_cors import CORS

import rest_api.config_endpoints
import rest_api.query_endpoints
import rest_api.catalogue_endpoints
import rest_api.images_endpoints

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "pocol-back"

rest_api.config_endpoints.prepare(app)
rest_api.query_endpoints.prepare(app)
rest_api.catalogue_endpoints.prepare(app)
rest_api.images_endpoints.prepare(app)