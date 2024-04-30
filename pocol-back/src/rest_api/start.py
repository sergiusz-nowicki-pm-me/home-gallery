from flask import Flask, send_file
from flask_cors import CORS

import rest_api.config_endpoints
import rest_api.query_endpoints

app = Flask(__name__)
CORS(app)

rest_api.config_endpoints.prepare(app)
rest_api.query_endpoints.prepare(app)