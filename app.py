from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
socketio = SocketIO(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    contact = db.Column(db.String(20), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = generate_password_hash(data['password'])
    contact = data['contact']
    
    user = User(username=username, password=password, contact=contact)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Login failed'}), 401

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_help')
def handle_send_help(json):
    latitude = json['latitude']
    longitude = json['longitude']
    print('Received help signal:', json)

    # Call the Nominatim API to reverse geocode the coordinates
    response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}")
    address_info = response.json().get('display_name', 'Address not found')

    emit('help_response', {'message': 'Help is on the way!', 'location': address_info})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)