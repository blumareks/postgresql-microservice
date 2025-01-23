# created by Marek Sadowski
# github: https://github.com/blumareks/postgresql-microservice
# Apache 2 Licence


#from asyncio.windows_events import NULL
from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

#import psycopg2
#from psycopg2 import sql
from dotenv import load_dotenv
import json
import os
import uuid
import csv
import io

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database configuration from the environment
URI = os.getenv("URL")


app = Flask(__name__)

# prepare SQLAlchemy DB
# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = URI; #'postgresql://username:password@localhost:5432/alerts_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(100), nullable=False)
    object_id = db.Column(db.String(100), nullable=False)
    impacted_device = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    additional_info = db.Column(db.Text, nullable=True)

# Initialize the database
# https://stackoverflow.com/questions/73961938/flask-sqlalchemy-db-create-all-raises-runtimeerror-working-outside-of-applicat
with app.app_context():
    db.create_all()


# create API
# Routes
@app.route('/newalert', methods=['POST'])
def create_alert():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid input, no JSON payload provided'}), 400

    try:
        alert = Alert(
            alert_id=data['alert_id'],
            object_id=data['object_id'],
            impacted_device=data['impacted_device'],
            description=data['description'],
            additional_info=data.get('additional_info', None)
        )
        db.session.add(alert)
        db.session.commit()
        return jsonify({'message': 'Alert created successfully', 'alert_id': alert.id}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# expose APIs
################



@app.route('/alerts/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404

    return jsonify({
        'alert_id': alert.alert_id,
        'object_id': alert.object_id,
        'impacted_device': alert.impacted_device,
        'description': alert.description,
        'additional_info': alert.additional_info
    })

@app.route('/alerts', methods=['GET'])
def list_alerts():
    print("GET alerts")
    alerts = Alert.query.all()
    return jsonify([{
        'alert_id': alert.alert_id,
        'object_id': alert.object_id,
        'impacted_device': alert.impacted_device,
        'description': alert.description,
        'additional_info': alert.additional_info
    } for alert in alerts])


@app.route('/alertspager', methods=['GET'])
def list_alerts_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Alert.query.paginate(page=page, per_page=per_page, error_out=False)

    alerts = [{
        'alert_id': alert.alert_id,
        'object_id': alert.object_id,
        'impacted_device': alert.impacted_device,
        'description': alert.description,
        'additional_info': alert.additional_info
    } for alert in pagination.items]

    next_url = url_for('list_alerts', page=pagination.next_num) if pagination.has_next else None
    total_pages = pagination.pages

    return jsonify({
        'alerts': alerts,
        'next_page': next_url,
        'total_pages': total_pages
    })

# Initialize the server and create the table if not already created
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5001, debug=True)
