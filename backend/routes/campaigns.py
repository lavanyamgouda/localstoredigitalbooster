from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from backend.config.db import get_db
from datetime import datetime

campaigns_bp = Blueprint('campaigns', __name__)

def serialize(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@campaigns_bp.route('/', methods=['GET'])
def get_campaigns():
    db = get_db()
    store_id = request.args.get('store_id', '')
    status = request.args.get('status', '')
    query = {}
    if store_id: query['store_id'] = store_id
    if status: query['status'] = status
    campaigns = list(db.campaigns.find(query).sort('created_at', -1))
    return jsonify([serialize(c) for c in campaigns]), 200

@campaigns_bp.route('/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    try:
        db = get_db()
        c = db.campaigns.find_one({'_id': ObjectId(campaign_id)})
        if not c:
            return jsonify({'error': 'Campaign not found'}), 404
        return jsonify(serialize(c)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400

@campaigns_bp.route('/', methods=['POST'])
def create_campaign():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if not data.get('name'):
        return jsonify({'error': 'Campaign name is required'}), 422
    now = datetime.utcnow().isoformat()
    db = get_db()
    doc = {
        'store_id': str(data.get('store_id', '')),
        'name': str(data.get('name', '')).strip(),
        'type': str(data.get('type', 'Social Media')),
        'budget': float(data.get('budget', 0)),
        'start_date': str(data.get('start_date', '')),
        'end_date': str(data.get('end_date', '')),
        'target_audience': str(data.get('target_audience', '')).strip(),
        'message': str(data.get('message', '')).strip(),
        'discount': str(data.get('discount', '')).strip(),
        'status': str(data.get('status', 'draft')),
        'impressions': int(data.get('impressions', 0)),
        'clicks': int(data.get('clicks', 0)),
        'conversions': int(data.get('conversions', 0)),
        'created_at': now,
        'updated_at': now,
    }
    result = db.campaigns.insert_one(doc)
    doc['_id'] = str(result.inserted_id)
    return jsonify(doc), 201

@campaigns_bp.route('/<campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    try:
        data = request.get_json()
        db = get_db()
        update = {
            'store_id': str(data.get('store_id', '')),
            'name': str(data.get('name', '')).strip(),
            'type': str(data.get('type', 'Social Media')),
            'budget': float(data.get('budget', 0)),
            'start_date': str(data.get('start_date', '')),
            'end_date': str(data.get('end_date', '')),
            'target_audience': str(data.get('target_audience', '')).strip(),
            'message': str(data.get('message', '')).strip(),
            'discount': str(data.get('discount', '')).strip(),
            'status': str(data.get('status', 'draft')),
            'updated_at': datetime.utcnow().isoformat(),
        }
        result = db.campaigns.update_one({'_id': ObjectId(campaign_id)}, {'$set': update})
        if result.matched_count == 0:
            return jsonify({'error': 'Campaign not found'}), 404
        updated = db.campaigns.find_one({'_id': ObjectId(campaign_id)})
        return jsonify(serialize(updated)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400

@campaigns_bp.route('/<campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    try:
        db = get_db()
        result = db.campaigns.delete_one({'_id': ObjectId(campaign_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Campaign not found'}), 404
        return jsonify({'message': 'Campaign deleted'}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400