from flask import Blueprint, jsonify, request
from backend.config.db import get_db
from datetime import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/summary', methods=['GET'])
def summary():
    db = get_db()
    total_stores = db.stores.count_documents({})
    active_stores = db.stores.count_documents({'active': True})
    total_products = db.products.count_documents({})
    low_stock = db.products.count_documents({'stock_qty': {'$lte': 5}})
    total_campaigns = db.campaigns.count_documents({})
    active_campaigns = db.campaigns.count_documents({'status': 'active'})
    return jsonify({
        'stores': {'total': total_stores, 'active': active_stores},
        'products': {'total': total_products, 'low_stock': low_stock},
        'campaigns': {'total': total_campaigns, 'active': active_campaigns},
        'avg_products_per_store': round(total_products / total_stores, 1) if total_stores else 0,
    }), 200

@analytics_bp.route('/stores-by-category', methods=['GET'])
def stores_by_category():
    db = get_db()
    pipeline = [
        {'$group': {'_id': '$category', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
    ]
    result = list(db.stores.aggregate(pipeline))
    return jsonify([{'category': r['_id'] or 'Other', 'count': r['count']} for r in result]), 200

@analytics_bp.route('/products-by-category', methods=['GET'])
def products_by_category():
    db = get_db()
    pipeline = [
        {'$group': {'_id': '$category', 'count': {'$sum': 1}, 'total_stock': {'$sum': '$stock_qty'}}},
        {'$sort': {'count': -1}},
    ]
    result = list(db.products.aggregate(pipeline))
    return jsonify([{'category': r['_id'] or 'Other', 'count': r['count'], 'total_stock': r['total_stock']} for r in result]), 200

@analytics_bp.route('/top-stores', methods=['GET'])
def top_stores():
    db = get_db()
    pipeline = [
        {'$group': {'_id': '$store_id', 'product_count': {'$sum': 1}}},
        {'$sort': {'product_count': -1}},
        {'$limit': 10},
    ]
    product_counts = {r['_id']: r['product_count'] for r in db.products.aggregate(pipeline)}
    stores = list(db.stores.find({}, {'name': 1, 'city': 1, 'category': 1, 'active': 1}))
    result = []
    for s in stores:
        sid = str(s['_id'])
        result.append({
            '_id': sid,
            'name': s['name'],
            'city': s.get('city', ''),
            'category': s.get('category', ''),
            'active': s.get('active', True),
            'product_count': product_counts.get(sid, 0),
        })
    result.sort(key=lambda x: x['product_count'], reverse=True)
    return jsonify(result[:10]), 200