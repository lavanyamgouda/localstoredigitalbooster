"""
backend/models/campaign.py
Campaign document schema and validation
"""

from datetime import datetime


def campaign_schema(data: dict) -> dict:
    return {
        'store_id':        str(data.get('store_id', '')).strip(),
        'name':            str(data.get('name', '')).strip(),
        'type':            str(data.get('type', 'Social Media')).strip(),
        'budget':          float(data.get('budget', 0)),
        'start_date':      str(data.get('start_date', '')),
        'end_date':        str(data.get('end_date', '')),
        'target_audience': str(data.get('target_audience', '')).strip(),
        'message':         str(data.get('message', '')).strip(),
        'discount':        str(data.get('discount', '')).strip(),
        'status':          str(data.get('status', 'draft')),
        'impressions':     int(data.get('impressions', 0)),
        'clicks':          int(data.get('clicks', 0)),
        'conversions':     int(data.get('conversions', 0)),
        'created_at':      data.get('created_at', datetime.utcnow().isoformat()),
        'updated_at':      datetime.utcnow().isoformat(),
    }


def validate_campaign(data: dict) -> list[str]:
    errors = []
    if not data.get('name'):       errors.append('Campaign name is required.')
    if not data.get('store_id'):   errors.append('Store is required.')
    if not data.get('start_date'): errors.append('Start date is required.')
    if not data.get('end_date'):   errors.append('End date is required.')
    if not data.get('message'):    errors.append('Campaign message is required.')
    return errors
