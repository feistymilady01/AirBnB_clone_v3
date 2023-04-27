#!/usr/bin/python3
"""
Review api Module
"""
import models
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place"""
    reviews = storage.all(Review)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_reviews = place.reviews
    reviewList = []
    for review in place_reviews:
        reviewList.append(review.to_dict())
    return jsonify(reviewList)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ Retrieve a review object by id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ Create a new instance of Review """
    if not request.json:
        abort(400, description='Not a JSON')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if 'user_id' not in request.json:
        abort(400, description='Missing user_id')
    data = request.get_json()
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in request.json:
        abort(400, description='Missing text')
    data['place_id'] = place_id
    new_review = Review(**data)  # initialized as kwargs
    new_review.save()
    # return make_response(jsonify(new_state.to_dict()), 201)
    # both works
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ Updates the attribute of a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, description='Not a JSON')
    reviewAttr = request.get_json()
    for key, value in reviewAttr.items():
        if key not in \
                {'id', 'created_at', 'updated_at', 'user_id', 'place_id'}:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return (jsonify({}), 200)
