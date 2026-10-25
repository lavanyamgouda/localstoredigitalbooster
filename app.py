from flask import Flask
from flask_cors import CORS
from backend.config.db import init_db
from backend.routes.stores import stores_bp
from backend.routes.products import products_bp
from backend.routes.payments import payments_bp
from backend.routes.orders import orders_bp
from backend.routes.campaigns import campaigns_bp
from backend.routes.analytics import analytics_bp

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

init_db(app)

app.register_blueprint(stores_bp,    url_prefix='/api/stores')
app.register_blueprint(products_bp,  url_prefix='/api/products')
app.register_blueprint(payments_bp,  url_prefix='/api/payments')
app.register_blueprint(orders_bp,    url_prefix='/api/orders')
app.register_blueprint(campaigns_bp, url_prefix='/api/campaigns')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

@app.route('/')
def index():
    return {'message': 'API running'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)