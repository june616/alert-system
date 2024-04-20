from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.json
        username = data['username']
        password = generate_password_hash(data['password'])
        contact = data['contact']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        user = User(username=username, password=password, contact=contact)
        db.session.add(user)
        db.session.commit()

        # return redirect(url_for('index'))
        return jsonify({'message': 'Registered successfully'}), 201


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.json
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            # return redirect(url_for('index'))
            return jsonify({'message': 'Login successful'}), 200
        else:
            # flash('Login failed. Please check your username and password and try again.')
            # return redirect(url_for('login'))
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

@socketio.on('help_signal')
def handle_help_signal(json):
    user_id = json.get('id')
    user = User.query.get(user_id)
    if user:
        emergency_contact = user.contact
        # Assume `json` contains `latitude` and `longitude`
        latitude = json.get('latitude')
        longitude = json.get('longitude')

        # You can also include code to reverse-geocode the coordinates to get a human-readable address
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
        )
        address_info = response.json().get('display_name', 'Address not found')

        # Generate an alert message or any other action required
        alert_message = f"Help needed for user: {user.username}, at location: {address_info}. " \
                        f"Emergency contact: {emergency_contact}"

        # Emit a response back to the frontend or broadcast to an admin panel if needed
        emit('help_response', {'message': alert_message})
    else:
        emit('help_response', {'message': 'User not found.'})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
