#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    # Query all bakeries from the database
    bakeries = Bakery.query.all()
    # Serialize the list of bakeries
    bakery_list = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakery_list)

# GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in a list
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
        # Query the bakery by its ID
    bakery = Bakery.query.get(id)
    if bakery:
        # Serialize the bakery with nested baked goods
        return jsonify(bakery.to_dict(nested=True))
    return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
        # Query all baked goods sorted by price in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # Serialize the list of baked goods
    baked_goods_list = [good.to_dict() for good in baked_goods]
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
        # Query the most expensive baked good
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        # Serialize the most expensive baked good
        return jsonify(most_expensive.to_dict())
    return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
