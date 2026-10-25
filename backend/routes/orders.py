from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from backend.config.db import get_db
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

def serialize(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@orders_bp.route('/', methods=['GET'])
def get_orders():
    db = get_db()
    store_id = request.args.get('store_id', '')
    status = request.args.get('status', '')
    query = {}
    if store_id: query['store_id'] = store_id
    if status: query['status'] = status
    orders = list(db.orders.find(query).sort('created_at', -1).limit(200))
    return jsonify([serialize(o) for o in orders]), 200

@orders_bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    try:
        db = get_db()
        order = db.orders.find_one({'_id': ObjectId(order_id)})
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify(serialize(order)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400

@orders_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if not data.get('customer_name'):
        return jsonify({'error': 'Customer name is required'}), 422
    now = datetime.utcnow().isoformat()
    db = get_db()
    doc = {
        'store_id': str(data.get('store_id', '')),
        'order_number': str(data.get('order_number', '')),
        'customer_name': str(data.get('customer_name', '')).strip(),
        'customer_phone': str(data.get('customer_phone', '')).strip(),
        'customer_address': str(data.get('customer_address', '')).strip(),
        'items': data.get('items', []),
        'subtotal': float(data.get('subtotal', 0)),
        'gst_percent': float(data.get('gst_percent', 0)),
        'gst_amount': float(data.get('gst_amount', 0)),
        'discount': float(data.get('discount', 0)),
        'grand_total': float(data.get('grand_total', 0)),
        'payment_method': str(data.get('payment_method', 'cash')),
        'status': str(data.get('status', 'completed')),
        'notes': str(data.get('notes', '')).strip(),
        'date': str(data.get('date', now[:10])),
        'created_at': now,
        'updated_at': now,
    }
    result = db.orders.insert_one(doc)
    doc['_id'] = str(result.inserted_id)
    return jsonify(doc), 201

@orders_bp.route('/<order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        data = request.get_json()
        db = get_db()
        update = {
            'store_id': str(data.get('store_id', '')),
            'customer_name': str(data.get('customer_name', '')).strip(),
            'customer_phone': str(data.get('customer_phone', '')).strip(),
            'customer_address': str(data.get('customer_address', '')).strip(),
            'items': data.get('items', []),
            'subtotal': float(data.get('subtotal', 0)),
            'gst_percent': float(data.get('gst_percent', 0)),
            'gst_amount': float(data.get('gst_amount', 0)),
            'discount': float(data.get('discount', 0)),
            'grand_total': float(data.get('grand_total', 0)),
            'payment_method': str(data.get('payment_method', 'cash')),
            'status': str(data.get('status', 'completed')),
            'notes': str(data.get('notes', '')).strip(),
            'updated_at': datetime.utcnow().isoformat(),
        }
        result = db.orders.update_one({'_id': ObjectId(order_id)}, {'$set': update})
        if result.matched_count == 0:
            return jsonify({'error': 'Order not found'}), 404
        updated = db.orders.find_one({'_id': ObjectId(order_id)})
        return jsonify(serialize(updated)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400

@orders_bp.route('/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        db = get_db()
        result = db.orders.delete_one({'_id': ObjectId(order_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify({'message': 'Order deleted'}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400