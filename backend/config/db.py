"""
backend/config/db.py
MongoDB connection using PyMongo
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

# Global db reference
_db = None

def init_db(app=None):
    """Initialize MongoDB connection."""
    global _db

    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    db_name   = os.environ.get('DB_NAME', 'digitalbooster')

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')   # Check connection
        _db = client[db_name]
        print(f"✅ Connected to MongoDB: {db_name}")

        # Create indexes
        _db.stores.create_index('name')
        _db.stores.create_index('city')
        _db.products.create_index('store_id')
        _db.products.create_index('name')
        _db.campaigns.create_index('store_id')

    except ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise


def get_db():
    """Return the database instance."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db
