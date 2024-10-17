from datetime import datetime
from . import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    prices = db.relationship('ProductTicket', back_populates='product')

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    description_id = db.Column(db.Integer, db.ForeignKey('description.id'))
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    local = db.Column(db.String(50), nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'))
    products = db.relationship('ProductTicket', back_populates='ticket')

class ProductTicket(db.Model):
    __tablename__ = 'product_ticket'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    
    product = db.relationship('Product', back_populates='prices')
    ticket = db.relationship('Ticket', back_populates='products')

class PaymentType(db.Model):
    __tablename__ = 'payment_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tickets = db.relationship('Ticket', backref='payment_type')

class Description(db.Model):
    __tablename__ = 'description'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    tickets = db.relationship('Ticket', backref='description')
