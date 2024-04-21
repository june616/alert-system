from flask import Flask, request, jsonify, render_template, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from twilio.rest import Client
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
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
        data = request.get_json()
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
            session['user_id'] = user.id
            # return redirect(url_for('index'))
            return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
        else:
            flash('Login failed. Please check your username and password and try again.')
            return jsonify({'message': 'Login failed'}), 401
            # return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@socketio.on('send_help')
def handle_send_help(json):
    user_id = json.get('id')
    latitude = json['latitude']
    longitude = json['longitude']
    user = User.query.get(user_id)
    
    if user:
        emit('status_update', {'message': 'Locating...'})
        response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}")
        address_info = response.json().get('display_name', 'Address not found')

        emergency_contact = user.contact
        alert_message = f"From Help Alert System: Emergency at {address_info}."
        emit('status_update', {'message': 'Sending SMS...'})

        send_sms(emergency_contact, alert_message)

        emit('help_response', {
            'message': 'Help is on the way!',
            'location': address_info,
            'sms_status': 'Message sent to ' + emergency_contact
        })
    else:
        emit('help_response', {'message': 'User not found.'})

def send_sms(contact, message):
    client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    message = client.messages.create(
        to=contact,
        from_=app.config['TWILIO_NUMBER'],
        body=message
    )
    print(f"send out message: to {message.to}, body {message.body}")
    return message.sid


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
