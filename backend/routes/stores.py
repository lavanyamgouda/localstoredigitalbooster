"""
backend/routes/stores.py
CRUD routes for stores: /api/stores
"""

from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from backend.config.db import get_db
from backend.models.store import store_schema, validate_store

stores_bp = Blueprint('stores', __name__)


def serialize(doc):
    """Convert MongoDB ObjectId to string."""
    doc['_id'] = str(doc['_id'])
    return doc


# ── GET all stores ──────────────────────────────────────────────
@stores_bp.route('/', methods=['GET'])
def get_stores():
    db = get_db()
    limit = int(request.args.get('limit', 0))
    city  = request.args.get('city', '')
    cat   = request.args.get('category', '')

    query = {}
    if city: query['city'] = {'$regex': city, '$options': 'i'}
    if cat:  query['category'] = cat

    cursor = db.stores.find(query).sort('created_at', -1)
    if limit: cursor = cursor.limit(limit)
    return jsonify([serialize(s) for s in cursor]), 200


# ── GET single store ────────────────────────────────────────────
@stores_bp.route('/<store_id>', methods=['GET'])
def get_store(store_id):
    try:
        db = get_db()
        store = db.stores.find_one({'_id': ObjectId(store_id)})
        if not store:
            return jsonify({'error': 'Store not found'}), 404
        return jsonify(serialize(store)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid store ID'}), 400


# ── POST create store ───────────────────────────────────────────
@stores_bp.route('/', methods=['POST'])
def create_store():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    errors = validate_store(data)
    if errors:
        return jsonify({'error': errors[0], 'errors': errors}), 422

    db = get_db()
    doc = store_schema(data)
    result = db.stores.insert_one(doc)
    doc['_id'] = str(result.inserted_id)
    return jsonify(doc), 201


# ── PUT update store ────────────────────────────────────────────
@stores_bp.route('/<store_id>', methods=['PUT'])
def update_store(store_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        errors = validate_store(data)
        if errors:
            return jsonify({'error': errors[0], 'errors': errors}), 422

        db = get_db()
        update_doc = store_schema(data)
        # Preserve original created_at
        del update_doc['created_at']

        result = db.stores.update_one(
            {'_id': ObjectId(store_id)},
            {'$set': update_doc}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Store not found'}), 404

        updated = db.stores.find_one({'_id': ObjectId(store_id)})
        return jsonify(serialize(updated)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid store ID'}), 400


# ── DELETE store ────────────────────────────────────────────────
@stores_bp.route('/<store_id>', methods=['DELETE'])
def delete_store(store_id):
    try:
        db = get_db()
        result = db.stores.delete_one({'_id': ObjectId(store_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Store not found'}), 404
        # Also delete store's products and campaigns
        db.products.delete_many({'store_id': store_id})
        db.campaigns.delete_many({'store_id': store_id})
        return jsonify({'message': 'Store deleted successfully'}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid store ID'}), 400


# ── PATCH toggle active ─────────────────────────────────────────
@stores_bp.route('/<store_id>/toggle', methods=['PATCH'])
def toggle_store(store_id):
    try:
        db = get_db()
        store = db.stores.find_one({'_id': ObjectId(store_id)})
        if not store:
            return jsonify({'error': 'Store not found'}), 404
        new_status = not store.get('active', True)
        db.stores.update_one({'_id': ObjectId(store_id)}, {'$set': {'active': new_status}})
        return jsonify({'active': new_status}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid store ID'}), 400
