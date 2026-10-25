"""
seed_data.py — Populate MongoDB with sample data for testing
Run: python seed_data.py
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient('mongodb://localhost:27017/')
db = client['digitalbooster']

# Clear existing
db.stores.delete_many({})
db.products.delete_many({})
db.campaigns.delete_many({})
print("🗑️  Cleared existing data")

# ── Stores ──────────────────────────────────────────────────────
stores_data = [
    {'name': 'Sharma General Store', 'owner_name': 'Ramesh Sharma', 'phone': '9876543210',
     'email': 'sharma@example.com', 'address': '12 MG Road', 'city': 'Bengaluru',
     'pincode': '560001', 'category': 'Grocery', 'gst_number': '29ABCDE1234F1Z5',
     'description': 'Your neighbourhood grocery store since 1995.', 'active': True},
    {'name': 'Patel Electronics', 'owner_name': 'Suresh Patel', 'phone': '9812345678',
     'email': 'patel@example.com', 'address': '45 Brigade Road', 'city': 'Bengaluru',
     'pincode': '560025', 'category': 'Electronics', 'gst_number': '29XYZAB5678G2Z6',
     'description': 'Best deals on electronics and gadgets.', 'active': True},
    {'name': 'Gupta Pharmacy', 'owner_name': 'Anjali Gupta', 'phone': '9988776655',
     'email': 'gupta@example.com', 'address': '8 Indiranagar', 'city': 'Bengaluru',
     'pincode': '560038', 'category': 'Pharmacy', 'gst_number': '29PHARMA789H3Z7',
     'description': 'Trusted pharmacy with wide range of medicines.', 'active': True},
    {'name': 'Yadav Fashion House', 'owner_name': 'Priya Yadav', 'phone': '9955443322',
     'email': 'yadav@example.com', 'address': '23 Koramangala', 'city': 'Bengaluru',
     'pincode': '560034', 'category': 'Clothing & Fashion', 'gst_number': '',
     'description': 'Trendy clothes for the whole family.', 'active': True},
    {'name': 'Reddy Tiffin Center', 'owner_name': 'Venkat Reddy', 'phone': '9900112233',
     'email': 'reddy@example.com', 'address': '5 JP Nagar', 'city': 'Bengaluru',
     'pincode': '560078', 'category': 'Restaurant / Food', 'gst_number': '',
     'description': 'Authentic South Indian tiffin and meals.', 'active': True},
]

now = datetime.utcnow().isoformat()
for s in stores_data:
    s['active'] = True
    s['created_at'] = now
    s['updated_at'] = now

result = db.stores.insert_many(stores_data)
store_ids = [str(oid) for oid in result.inserted_ids]
print(f"✅ Inserted {len(store_ids)} stores")

# ── Products ─────────────────────────────────────────────────────
products_data = [
    # Grocery
    {'store_id': store_ids[0], 'name': 'Tata Salt 1kg', 'sku': 'SALT001', 'price': 25, 'mrp': 28, 'stock_qty': 150, 'unit': 'pcs', 'category': 'Groceries'},
    {'store_id': store_ids[0], 'name': 'Aashirvaad Atta 5kg', 'sku': 'ATTA001', 'price': 280, 'mrp': 310, 'stock_qty': 60, 'unit': 'pcs', 'category': 'Groceries'},
    {'store_id': store_ids[0], 'name': 'Amul Butter 500g', 'sku': 'BUT001', 'price': 250, 'mrp': 265, 'stock_qty': 30, 'unit': 'pcs', 'category': 'Dairy'},
    {'store_id': store_ids[0], 'name': 'Parle-G Biscuits', 'sku': 'BISC001', 'price': 10, 'mrp': 10, 'stock_qty': 200, 'unit': 'pcs', 'category': 'Snacks'},
    {'store_id': store_ids[0], 'name': 'Sunrise Refined Oil 1L', 'sku': 'OIL001', 'price': 145, 'mrp': 160, 'stock_qty': 45, 'unit': 'pcs', 'category': 'Groceries'},
    # Electronics
    {'store_id': store_ids[1], 'name': 'Samsung USB-C Charger 25W', 'sku': 'CHRG001', 'price': 1299, 'mrp': 1499, 'stock_qty': 20, 'unit': 'pcs', 'category': 'Electronics'},
    {'store_id': store_ids[1], 'name': 'boAt Airdopes 141', 'sku': 'TWS001', 'price': 999, 'mrp': 1499, 'stock_qty': 15, 'unit': 'pcs', 'category': 'Electronics'},
    {'store_id': store_ids[1], 'name': 'Mi Power Bank 10000mAh', 'sku': 'PWR001', 'price': 799, 'mrp': 999, 'stock_qty': 8, 'unit': 'pcs', 'category': 'Electronics'},
    # Pharmacy
    {'store_id': store_ids[2], 'name': 'Dolo 650 Strip', 'sku': 'MED001', 'price': 30, 'mrp': 35, 'stock_qty': 100, 'unit': 'pcs', 'category': 'Medicines'},
    {'store_id': store_ids[2], 'name': 'Vitamin C 500mg (30 tabs)', 'sku': 'VIT001', 'price': 120, 'mrp': 140, 'stock_qty': 50, 'unit': 'pcs', 'category': 'Medicines'},
    {'store_id': store_ids[2], 'name': 'Savlon Antiseptic 250ml', 'sku': 'SAV001', 'price': 95, 'mrp': 110, 'stock_qty': 3, 'unit': 'pcs', 'category': 'Medicines'},
    # Fashion
    {'store_id': store_ids[3], 'name': 'Cotton Kurti (Ladies)', 'sku': 'KUR001', 'price': 599, 'mrp': 799, 'stock_qty': 25, 'unit': 'pcs', 'category': 'Clothing'},
    {'store_id': store_ids[3], 'name': 'Jeans Regular Fit', 'sku': 'JNS001', 'price': 899, 'mrp': 1199, 'stock_qty': 18, 'unit': 'pcs', 'category': 'Clothing'},
]

for p in products_data:
    p['active'] = True
    p['created_at'] = now
    p['updated_at'] = now
    p['image_url'] = ''
    p.setdefault('description', '')

db.products.insert_many(products_data)
print(f"✅ Inserted {len(products_data)} products")

# ── Campaigns ────────────────────────────────────────────────────
today = datetime.utcnow()
campaigns_data = [
    {
        'store_id': store_ids[0], 'name': 'Diwali Mega Sale', 'type': 'WhatsApp',
        'budget': 5000, 'start_date': (today - timedelta(days=2)).isoformat(),
        'end_date': (today + timedelta(days=5)).isoformat(),
        'target_audience': 'Local residents within 3km',
        'message': 'Celebrate Diwali with us! Flat 20% off on all grocery items.',
        'discount': '20% off on all items', 'status': 'active',
        'impressions': 1240, 'clicks': 320, 'conversions': 85,
    },
    {
        'store_id': store_ids[1], 'name': 'Weekend Electronics Bonanza', 'type': 'Social Media',
        'budget': 3000, 'start_date': (today - timedelta(days=1)).isoformat(),
        'end_date': (today + timedelta(days=2)).isoformat(),
        'target_audience': 'Tech enthusiasts 18-35',
        'message': 'Huge discounts on earphones, chargers, and power banks!',
        'discount': 'Up to 30% off', 'status': 'active',
        'impressions': 890, 'clicks': 210, 'conversions': 42,
    },
    {
        'store_id': store_ids[2], 'name': 'Health Awareness Camp', 'type': 'Flyer / Poster',
        'budget': 1500, 'start_date': (today + timedelta(days=7)).isoformat(),
        'end_date': (today + timedelta(days=14)).isoformat(),
        'target_audience': 'All age groups',
        'message': 'Free BP and sugar check-up. Buy medicines and get 10% off.',
        'discount': '10% off on medicines', 'status': 'draft',
        'impressions': 0, 'clicks': 0, 'conversions': 0,
    },
]

for c in campaigns_data:
    c['created_at'] = now
    c['updated_at'] = now

db.campaigns.insert_many(campaigns_data)
print(f"✅ Inserted {len(campaigns_data)} campaigns")
print("\n🎉 Seed data inserted successfully! Start the Flask app and open the frontend.")
