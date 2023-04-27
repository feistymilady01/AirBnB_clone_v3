#!/usr/bin/python3
"""
Amenity api Module
"""
import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity)
    amenityList = []
    if amenities is None:
        abort(404)
    for amenity in amenities.values():
        amenityList.append(amenity.to_dict())
    return jsonify(amenityList)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieve an amenity object by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ Create a new instance of Amenity """
    if not request.json:
        abort(400, description='Not a JSON')
    if 'name' not in request.json:
        abort(400, description='Missing name')
    amenityAttr = request.get_json()
    new_amenity = Amenity(**amenityAttr)  # initialized as kwargs
    print(new_amenity)
    new_amenity.save()
    # return make_response(jsonify(new_state.to_dict()), 201)
    # both works
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates the attribute of am amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    amenityAttr = request.get_json()
    for key, value in amenityAttr.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)
