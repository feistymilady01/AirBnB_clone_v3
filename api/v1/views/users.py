#!/usr/bin/python3
"""
Users api Module
"""
import models
from models import storage
from models.user import User
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User)
    userList = []
    if users is None:
        abort(404)
    for user in users.values():
        userList.append(user.to_dict())
    return jsonify(userList)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Retrieve a user object by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'])
def create_user():
    """ Create a new instance of User """
    if not request.json:
        abort(400, description='Not a JSON')
    if 'email' not in request.json:
        abort(400, description='Missing email')
    if 'password' not in request.json:
        abort(400, description='Missing password')
    userAttr = request.get_json()
    new_user = User(**userAttr)  # initialized as kwargs
    new_user.save()
    # return make_response(jsonify(new_state.to_dict()), 201)
    # both works
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Updates the attribute of a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    userAttr = request.get_json()
    for key, value in userAttr.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}), 200)
