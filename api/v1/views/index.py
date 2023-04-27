#!/usr/bin/python3
"""
Blueprint resource for the api status
"""
import models
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ Returns the status of the api """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def obj_stat():
    """ Retrieves the number of each object by type """
    # import model
    from models.engine.db_storage import classes
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    # classes = models.engine.db_storage.classes
    # from models import storage, classes
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User}
    stats = {}
    for clss in classes:
        # stats[clss] = models.storage.count(clas)
        stats[clss] = models.storage.count(classes[clss])
    return jsonify(stats)
