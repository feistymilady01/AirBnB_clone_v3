#!/usr/bin/python3
"""
Main Flask app module
"""
from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
# app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


HBNB_API_HOST = getenv('HBNB_API_HOST') or '0.0.0.0'
HBNB_API_PORT = getenv('HBNB_API_PORT') or 5000


@app.teardown_appcontext
def session_handler(self):
    """ Close existing session of the sqlalchemy """
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """ Page Not Found handler """
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
