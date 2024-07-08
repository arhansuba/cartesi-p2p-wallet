# backend/auth/auth.py

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta

# Example secret key (replace with your actual secret key)
SECRET_KEY = 'your_secret_key'

def generate_jwt_token(user_id):
    """
    Generate JWT token for authentication.
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),  # Token expiration time
            'iat': datetime.utcnow(),  # Token issued at time
            'sub': user_id  # Subject of the token (user ID)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')
    except Exception as e:
        return str(e)

def verify_jwt_token(token):
    """
    Verify JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def login_required(func):
    """
    Decorator to ensure login is required for access.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = verify_jwt_token(token)
        if isinstance(user_id, str):
            return jsonify({'error': user_id}), 401
        
        # Optionally, you can pass the user_id to the wrapped function
        kwargs['user_id'] = user_id
        
        return func(*args, **kwargs)
    
    return decorated_function
