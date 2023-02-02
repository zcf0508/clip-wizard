import os
import sys

from flask import Flask


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join('./', relative_path)


app = Flask(__name__, static_url_path="", static_folder=resource_path('static'))

@app.route('/')
def index():
    return app.send_static_file('index.html')
