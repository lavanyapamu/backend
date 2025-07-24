
from flask import Blueprint, request, jsonify, current_app as app
from sqlalchemy import or_
from app.main.models.user import User
from app.main.models.roles import Role
from init_db import db
from datetime import timedelta
from init_db import mail, bcrypt
from flask_mail import Message
from itsdangerous import SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash
from flask import redirect
from itsdangerous import URLSafeTimedSerializer
from flask_cors import CORS
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth_bp', __name__)


def get_serializer():
        return URLSafeTimedSerializer(app.config['SECRET_KEY'])

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role_name')

   
    role_name = data.get('role_name', '').lower() 

    role = Role.query.filter_by(role_name=role_name).first()

   
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
       return jsonify({'message': 'User already exists with this email'}), 409
    

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(full_name=full_name, email=email, password=hashed_password, role_id=role.role_id, is_verified=False)
        db.session.add(new_user)
        db.session.commit()
       
        print(email)
        token = get_serializer().dumps(email, salt='email-confirm')

       
        verify_url = f"{app.config['FRONTEND_URL']}/emailverify?token={token}"

        msg = Message(
            subject='Verify your email for ArtFlare',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            body=f'Hi {full_name}, please verify your email by clicking this link: {verify_url}'
        )
        mail.send(msg)
        print("Verification URL:", verify_url)

        return jsonify({'message': 'User registered successfully. Please check your email to verify your account.'}), 201
    
    except Exception as e:
        db.session.rollback()
        return {"error": f"Registration failed: {str(e)}"}, 500


@auth_bp.route('/login', methods=['POST'])


def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

 
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

 
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found with this email'}), 404

    
    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 401

    
    if not user.is_verified:
        return jsonify({'message': 'Please verify your email before logging in'}), 403

    
    access_token = create_access_token(
        identity={
        'user_id': str(user.user_id),
        'role_id': user.role_id,
        
    }, expires_delta=timedelta(days=30) )
    print(access_token)
  
    return jsonify({
        'token': access_token,
        'user_id': str(user.user_id),
        'role_id': user.role_id,
      
    }), 200


@auth_bp.route('/emailverify/<token>', methods=['GET'])

def verify_email(token):
    try:
        email =  get_serializer().loads(token, salt='email-confirm', max_age=36000000)  # 11 hour valid
    except SignatureExpired:
        return jsonify({'message': 'Verification link expired'}), 400
    except BadSignature:
        return jsonify({'message': 'Invalid token'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.is_verified = True
    db.session.commit()
    return jsonify({'message': 'Email verified'}), 200


from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found with this email'}), 404

    # Generate reset token
    token = create_access_token(
        identity=email,
        expires_delta=timedelta(minutes=36000),
        additional_claims={"reset": True}
    )

    reset_link = f"{app.config['FRONTEND_URL']}/reset-password?token={token}"

    # Send reset email
    msg = Message(
        subject='Reset Your Password - ArtFlare',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email],
        body=f'Hi {user.full_name},\n\nClick the link below to reset your password:\n{reset_link}\n\nThis link is valid for 15 minutes.'
    )
    mail.send(msg)

    return jsonify({'message': 'Password reset link has been sent to your email.'}), 200



@auth_bp.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    jwt_data = get_jwt()
    if not jwt_data.get("reset"):
        return jsonify({'message': 'Invalid reset token'}), 401

    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({'message': 'New password is required'}), 400

    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200
