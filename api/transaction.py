from flask import Blueprint, request, jsonify
from datetime import datetime
from . import db
from .models import Transaction
from .auth import login_required

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('/', methods=['POST'])
@login_required
def create_transaction():
    """
    Endpoint to create a new transaction.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Extract transaction details from request data
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    amount = data.get('amount')

    # Perform validation (e.g., check if sender has sufficient balance)

    # Create a new transaction record
    new_transaction = Transaction(
        sender_id=sender_id,
        recipient_id=recipient_id,
        amount=amount,
        timestamp=datetime.utcnow()
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction created successfully'}), 201

@transactions_bp.route('/', methods=['GET'])
@login_required
def get_transactions():
    """
    Endpoint to fetch all transactions.
    """
    transactions = Transaction.query.all()
    return jsonify([transaction.to_dict() for transaction in transactions]), 200

# Add more endpoints as needed (e.g., fetch transaction by ID, update transaction, etc.)
