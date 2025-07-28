from flask import Blueprint, render_template, request, jsonify
from app.models.user import User
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/join-waitlist', methods=['POST'])
def join_waitlist():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(email=email, name=name)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Successfully joined waitlist'}), 200 