#!/usr/bin/python3
"""
city api Module
"""
import models
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views

app_views.strict_slashes = False


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """ Retrieves the list of all State objects """
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    """
    for city in cities.values():
        city = city.to_dict()
        # if str(state_id) == city['state_id']:
        if state_id in city.values():
            print(city)
    """
    # print(state)
    cities = state.cities
    # print(cities_)
    cityList = []
    for city in cities:
        cityList.append(city.to_dict())
    return jsonify(cityList)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ Retrieve a city object by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Create a new instance of state """
    if not request.json:
        abort(400, description='Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if 'name' not in request.json:
        abort(400, description='Missing name')

    city = request.get_json()
    city['state_id'] = state_id
    new_city = City(**city)  # initialized as kwargs
    new_city.save()
    # return make_response(jsonify(new_state.to_dict()), 201)
    # both works
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Updates the attribute of a state object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    cityAttr = request.get_json()
    for key, value in cityAttr.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            # for k, v in cityAttr.items():
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)
