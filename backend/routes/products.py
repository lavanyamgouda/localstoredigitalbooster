"""
backend/routes/products.py
CRUD routes for products: /api/products
"""

from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from backend.config.db import get_db
from backend.models.product import product_schema, validate_product

products_bp = Blueprint('products', __name__)


def serialize(doc):
    doc['_id'] = str(doc['_id'])
    return doc


# ── GET all products ────────────────────────────────────────────
@products_bp.route('/', methods=['GET'])
def get_products():
    db = get_db()
    store_id = request.args.get('store_id', '')
    category = request.args.get('category', '')
    low_stock = request.args.get('low_stock', '')
    limit = int(request.args.get('limit', 0))

    query = {}
    if store_id: query['store_id'] = store_id
    if category: query['category'] = category
    if low_stock: query['stock_qty'] = {'$lte': int(low_stock)}

    cursor = db.products.find(query).sort('created_at', -1)
    if limit: cursor = cursor.limit(limit)
    return jsonify([serialize(p) for p in cursor]), 200


# ── GET single product ──────────────────────────────────────────
@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        db = get_db()
        product = db.products.find_one({'_id': ObjectId(product_id)})
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(serialize(product)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid product ID'}), 400


# ── POST create product ─────────────────────────────────────────
@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    errors = validate_product(data)
    if errors:
        return jsonify({'error': errors[0], 'errors': errors}), 422

    db = get_db()
    # Verify store exists
    try:
        store = db.stores.find_one({'_id': ObjectId(data['store_id'])})
        if not store:
            return jsonify({'error': 'Store not found'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid store ID'}), 400

    doc = product_schema(data)
    result = db.products.insert_one(doc)
    doc['_id'] = str(result.inserted_id)
    return jsonify(doc), 201


# ── PUT update product ──────────────────────────────────────────
@products_bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        errors = validate_product(data)
        if errors:
            return jsonify({'error': errors[0], 'errors': errors}), 422

        db = get_db()
        update_doc = product_schema(data)
        del update_doc['created_at']

        result = db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_doc}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Product not found'}), 404

        updated = db.products.find_one({'_id': ObjectId(product_id)})
        return jsonify(serialize(updated)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid product ID'}), 400


# ── DELETE product ──────────────────────────────────────────────
@products_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        db = get_db()
        result = db.products.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'message': 'Product deleted'}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid product ID'}), 400


# ── PATCH update stock ──────────────────────────────────────────
@products_bp.route('/<product_id>/stock', methods=['PATCH'])
def update_stock(product_id):
    try:
        data = request.get_json()
        qty = data.get('stock_qty')
        if qty is None:
            return jsonify({'error': 'stock_qty is required'}), 400

        db = get_db()
        result = db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': {'stock_qty': int(qty)}}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'stock_qty': int(qty)}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid product ID'}), 400
