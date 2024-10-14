from . import db
from sqlalchemy import Numeric

# Modelo para la Descripción de Productos
class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# Modelo para el Tipo de Pago
class PaymentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

# Modelo para el Ticket
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description_id = db.Column(db.Integer, db.ForeignKey('description.id'), nullable=False)
    total_amount = db.Column(Numeric(10, 2), nullable=False)  # Ajuste para moneda
    date = db.Column(db.Date, nullable=False)
    local = db.Column(db.String(100), nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'), nullable=False)
    payment_type = db.relationship('PaymentType')
    description = db.relationship('Description')
    products = db.relationship('Product', backref='ticket', lazy=True)

# Modelo para cada Producto dentro del Ticket
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(Numeric(10, 2), nullable=False)  # Cantidad del producto
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    prices = db.relationship('ProductPrice', backref='product', lazy=True)

# Modelo para almacenar el Histórico de Precios
class ProductPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)  # Ajuste para moneda
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
