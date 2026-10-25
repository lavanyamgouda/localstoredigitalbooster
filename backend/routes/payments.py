"""
backend/routes/payments.py
Payment routes: /api/payments
"""

from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from backend.config.db import get_db
from datetime import datetime

payments_bp = Blueprint('payments', __name__)


def serialize(doc):
    doc['_id'] = str(doc['_id'])
    return doc


# ── GET all payments ────────────────────────────────────────────
@payments_bp.route('/', methods=['GET'])
def get_payments():
    db = get_db()
    store_id = request.args.get('store_id', '')
    status   = request.args.get('status', '')
    query = {}
    if store_id: query['store_id'] = store_id
    if status:   query['status']   = status
    payments = list(db.payments.find(query).sort('created_at', -1).limit(100))
    return jsonify([serialize(p) for p in payments]), 200


# ── GET single payment ──────────────────────────────────────────
@payments_bp.route('/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    try:
        db = get_db()
        payment = db.payments.find_one({'_id': ObjectId(payment_id)})
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        return jsonify(serialize(payment)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid payment ID'}), 400


# ── POST create payment record ──────────────────────────────────
@payments_bp.route('/', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if not data.get('customer_name') or not data.get('amount'):
        return jsonify({'error': 'Customer name and amount are required'}), 422

    db = get_db()
    now = datetime.utcnow().isoformat()
    doc = {
        'store_id':            str(data.get('store_id', '')),
        'customer_name':       str(data.get('customer_name', '')).strip(),
        'customer_phone':      str(data.get('customer_phone', '')).strip(),
        'customer_email':      str(data.get('customer_email', '')).strip().lower(),
        'amount':              float(data.get('amount', 0)),
        'description':         str(data.get('description', '')).strip(),
        'status':              str(data.get('status', 'pending')),
        'razorpay_payment_id': str(data.get('razorpay_payment_id', '')),
        'razorpay_order_id':   str(data.get('razorpay_order_id', '')),
        'created_at':          now,
        'updated_at':          now,
    }
    result = db.payments.insert_one(doc)
    doc['_id'] = str(result.inserted_id)
    return jsonify(doc), 201


# ── PUT update payment (status, razorpay ID) ───────────────────
@payments_bp.route('/<payment_id>', methods=['PUT'])
def update_payment(payment_id):
    try:
        data = request.get_json()
        db = get_db()
        update = {
            'status':              data.get('status', 'pending'),
            'razorpay_payment_id': data.get('razorpay_payment_id', ''),
            'razorpay_order_id':   data.get('razorpay_order_id', ''),
            'updated_at':          datetime.utcnow().isoformat(),
        }
        result = db.payments.update_one(
            {'_id': ObjectId(payment_id)},
            {'$set': update}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Payment not found'}), 404
        updated = db.payments.find_one({'_id': ObjectId(payment_id)})
        return jsonify(serialize(updated)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid payment ID'}), 400


# ── DELETE payment ──────────────────────────────────────────────
@payments_bp.route('/<payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    try:
        db = get_db()
        result = db.payments.delete_one({'_id': ObjectId(payment_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Payment not found'}), 404
        return jsonify({'message': 'Payment deleted'}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid payment ID'}), 400


# ── GET payment summary ─────────────────────────────────────────
@payments_bp.route('/summary', methods=['GET'])
def payment_summary():
    db = get_db()
    store_id = request.args.get('store_id', '')
    query = {}
    if store_id: query['store_id'] = store_id

    all_payments = list(db.payments.find(query))
    success  = [p for p in all_payments if p.get('status') == 'success']
    pending  = [p for p in all_payments if p.get('status') == 'pending']
    failed   = [p for p in all_payments if p.get('status') == 'failed']
    total_amount = sum(p.get('amount', 0) for p in success)

    return jsonify({
        'total':        len(all_payments),
        'success':      len(success),
        'pending':      len(pending),
        'failed':       len(failed),
        'total_amount': total_amount,
    }), 200