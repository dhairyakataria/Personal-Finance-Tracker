from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True,nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return str(self.user_id)

class Account(db.Model):
    __tablename__ = 'account'

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, default = 0.0)

class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    subcategories = db.relationship('Subcategory', backref='category', lazy=True)

class Subcategory(db.Model):
    __tablename__ = 'subcategory'

    subcategory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transaction'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.subcategory_id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    currency = db.Column(db.String(10), nullable=False)
