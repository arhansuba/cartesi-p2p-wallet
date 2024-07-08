# backend/models/user.py

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    @hybrid_property
    def password(self):
        # Make the password property read-only
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, plaintext_password):
        # Hash the password before saving
        self.password_hash = generate_password_hash(plaintext_password)

    def verify_password(self, plaintext_password):
        # Verify if the provided password matches the hashed password
        return check_password_hash(self.password_hash, plaintext_password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }
