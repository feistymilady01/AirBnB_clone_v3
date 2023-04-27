#!/usr/bin/python3
"""
Place api Module
"""
import models
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """ Retrieves the list of all Place objects """
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    """
    for city in cities.values():
        city = city.to_dict()
        # if str(state_id) == city['state_id']:
        if state_id in city.values():
            print(city)
    """
    # print(state)
    places = city.places
    # print(cities_)
    placeList = []
    for place in places:
        placeList.append(place.to_dict())
    return jsonify(placeList)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ Retrieve a place object by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Create a new instance of state """
    if not request.json:
        abort(400, description='Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if 'name' not in request.json:
        abort(400, description='Missing name')
    if 'user_id' not in request.json:
        abort(400, description='Missing user_id')
    # user = storage.get(User, user_id
    data = request.get_json()
    data['city_id'] = city_id
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_place = Place(**data)  # initialized as kwargs
    new_place.save()
    # return make_response(jsonify(new_state.to_dict()), 201)
    # both works
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ Updates the attribute of a state object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    placeAttr = request.get_json()
    for key, value in placeAttr.items():
        if key not in \
                {'id', 'created_at', 'updated_at', 'user_id', 'city_id'}:
            # for k, v in cityAttr.items():
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route(
        '/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}), 200)
