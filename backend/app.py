# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_cors import CORS

from routes.employee_routes import employee_bp
from routes.customer_routes import customer_bp
from routes.good_routes import good_bp
from routes.purchase_routes import purchase_bp
from routes.statistics_routes import statistics_bp
from routes.export_routes import export_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(good_bp, url_prefix='/api/goods')
    app.register_blueprint(purchase_bp, url_prefix='/api/purchases')
    app.register_blueprint(statistics_bp, url_prefix='/api/statistics')
    app.register_blueprint(export_bp, url_prefix='/api/export')

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'msg': 'SuperMarket API is running',
            'database': 'design'
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)