from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/static', static_folder="../static")
CORS(app)

app.debug = True
