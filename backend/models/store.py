"""
backend/models/store.py
Store document schema and helper functions
"""

from datetime import datetime


def store_schema(data: dict) -> dict:
    """Build a validated store document."""
    return {
        'name':        str(data.get('name', '')).strip(),
        'owner_name':  str(data.get('owner_name', '')).strip(),
        'phone':       str(data.get('phone', '')).strip(),
        'email':       str(data.get('email', '')).strip().lower(),
        'address':     str(data.get('address', '')).strip(),
        'city':        str(data.get('city', '')).strip(),
        'pincode':     str(data.get('pincode', '')).strip(),
        'category':    str(data.get('category', '')).strip(),
        'gst_number':  str(data.get('gst_number', '')).strip().upper(),
        'description': str(data.get('description', '')).strip(),
        'active':      bool(data.get('active', True)),
        'created_at':  data.get('created_at', datetime.utcnow().isoformat()),
        'updated_at':  datetime.utcnow().isoformat(),
    }


def validate_store(data: dict) -> list[str]:
    """Return a list of validation errors."""
    errors = []
    if not data.get('name'):       errors.append('Store name is required.')
    if not data.get('owner_name'): errors.append('Owner name is required.')
    if not data.get('phone'):      errors.append('Phone number is required.')
    if not data.get('address'):    errors.append('Address is required.')
    if not data.get('city'):       errors.append('City is required.')
    return errors
