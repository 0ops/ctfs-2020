from flask import Flask
from app import routes
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(routes.front, url_prefix="/renderer")
app.config["FLAG"] = os.getenv("FLAG", "CODEGATE2020{}")
