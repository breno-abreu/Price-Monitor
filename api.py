from flask import Flask, request, jsonify
import psycopg2
from dotenv import load_dotenv
import os
from marshmallow import Schema, fields, ValidationError
from subscribe import post_subscribers, get_subscribers
from price_data import get_price

app = Flask(__name__)

class SubscriptionSchema(Schema):
    link = fields.String(required=True)
    element_name = fields.String(required=True)
    element_type = fields.String(required=True)
    site_name = fields.String(required=False)


@app.route('/subscribers', methods=['POST', 'GET'])
def subscribers():
    if request.method == 'POST':
        payload = request.get_json()
        schema = SubscriptionSchema()

        try:
            # Dictionary with the data that was validated previously
            payload = schema.load(payload)
            post_subscribers(
                payload['link'],
                payload['element_name'],
                payload['element_type'],
                payload['site_name']
            )

            response = {'item': f"{payload['link']} {payload['element_name']} {payload['element_type']} {payload['site_name']}"}

            return jsonify(response), 201
                    
        # If the data is not valid, returns the error
        except ValidationError as err:
            return jsonify(err.messages), 400

        # Returns any other error that might occur
        except Exception as err:
            return jsonify(err.message)
    
    elif request.method == 'GET':
        try:
            return jsonify(get_subscribers()), 200
        
        # Returns any other error that might occur
        except Exception as err:
            return jsonify(err.message), 404


@app.route('/price', methods=['GET'])
def price():
    if request.method == 'GET':
        payload = request.args
        schema = SubscriptionSchema()

        try:
            # Dictionary with the data that was validated previously
            payload = schema.load(payload)
            price_date = get_price(
                payload['link'],
                payload['element_name'],
                payload['element_type'],
            )

            response = {
                'link': payload['link'],
                'price': price_date['price'],
                'date': price_date['date'],
                'site': payload['site_name']
            }

            return jsonify(response), 201
                    
        # If the data is not valid, returns the error
        except ValidationError as err:
            return jsonify(err.messages), 400

        # Returns any other error that might occur
        except Exception as err:
            return {'error': str(err)}, 404

