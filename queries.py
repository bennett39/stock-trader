from config import db
from models import User, Stock, Transaction
from sqlalchemy.sql import func

def insert_stock(symbol, name):
    stock = Stock(symbol=symbol, name=name)
    db.session.add(stock)
    db.session.commit()

def insert_transaction(user_id, stock_id, quantity, price):
    transaction = Transaction(user_id=user_id, stock_id=stock_id,
            quantity=quantity, price=price)
    db.session.add(transaction)
    db.session.commit()

def insert_user(username, password_hash):
    """Create new user"""
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

def select_user_by_id(user_id):
    """Get user object."""
    return User.query.filter_by(id=user_id).first()

def select_user_by_username(username):
    """Get user object."""
    return User.query.filter_by(username=username).first()

def select_stock_by_symbol(symbol):
    return Stock.query.filter_by(symbol=symbol).first()

def select_stocks_by_user(user):
    """Get list of stocks owned by a given user."""
    return (db.session.query(
                func.sum(Transaction.quantity).label('quantity'),
                Stock.name,
                Stock.symbol,
            ).join(User).join(Stock).group_by(
                Transaction.stock_id, Stock, User
            ).filter(User.id==user.id).all())

def select_transactions_by_user(user_id):
    """Get a list of all a user's transactions"""
    return (db.session.query(
                Transaction.id,
                Transaction.quantity,
                Transaction.price,
                Transaction.time,
                Stock.name,
                Stock.symbol,
            ).join(Stock).filter(
                Transaction.user_id==user_id
            ).all())


def select_transactions_by_stock(stock, user_id):
    """Get the sum of all a user's transactions of a certain stock"""
    return (db.session.query(
                func.sum(Transaction.quantity).label('shares')
            ).group_by(
                Transaction.stock_id    
            ).filter(
                Transaction.stock_id == stock.id,
                Transaction.user_id == user_id
            ).one())

def update_user_cash(change, user_id):
    user = select_user_by_id(user_id)
    user.cash = user.cash + change
    db.session.commit()
