from flask import Blueprint, request, jsonify
from .services import *

events_bp = Blueprint('events', __name__)

# GET all
@events_bp.route('/events', methods=['GET'])
def get_all():
    return jsonify(get_all_events())

# GET one
@events_bp.route('/events/<id>', methods=['GET'])
def get_one(id):
    event = get_event(id)
    if not event:
        return jsonify({"error": "Not found"}), 404
    return jsonify(event)

# CREATE
@events_bp.route('/events', methods=['POST'])
def create():
    data = request.json
    return jsonify(create_event(data)), 201

# UPDATE
@events_bp.route('/events/<id>', methods=['PUT'])
def update(id):
    updated = update_event(id, request.json)
    if not updated:
        return jsonify({"error": "Not found"}), 404
    return jsonify(updated)

# DELETE
@events_bp.route('/events/<id>', methods=['DELETE'])
def delete(id):
    success = delete_event(id)
    if not success:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"})
