"""
backend/models/product.py
Product document schema and validation
"""

from datetime import datetime


def product_schema(data: dict) -> dict:
    return {
        'store_id':    str(data.get('store_id', '')).strip(),
        'name':        str(data.get('name', '')).strip(),
        'sku':         str(data.get('sku', '')).strip().upper(),
        'price':       float(data.get('price', 0)),
        'mrp':         float(data.get('mrp', 0)),
        'stock_qty':   int(data.get('stock_qty', 0)),
        'unit':        str(data.get('unit', 'pcs')).strip(),
        'category':    str(data.get('category', '')).strip(),
        'description': str(data.get('description', '')).strip(),
        'image_url':   str(data.get('image_url', '')).strip(),
        'active':      bool(data.get('active', True)),
        'created_at':  data.get('created_at', datetime.utcnow().isoformat()),
        'updated_at':  datetime.utcnow().isoformat(),
    }


def validate_product(data: dict) -> list[str]:
    errors = []
    if not data.get('store_id'): errors.append('Store ID is required.')
    if not data.get('name'):     errors.append('Product name is required.')
    if float(data.get('price', 0)) <= 0:
        errors.append('Price must be greater than 0.')
    return errors
