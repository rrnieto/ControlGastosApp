from flask import Blueprint, render_template, request, redirect, url_for
from .models import Ticket, Product, ProductPrice, PaymentType, Description
from . import db
from datetime import datetime
import json

bp = Blueprint('main', __name__)

@bp.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Obtener datos del formulario
        description_existing_id = request.form.get('description_existing')
        description_new = request.form.get('description_new').strip()

        # Determinar la descripción del ticket
        if description_existing_id:
            description = Description.query.get(description_existing_id)
        elif description_new:
            description = Description.query.filter_by(name=description_new).first()
            if not description:
                description = Description(name=description_new)
                db.session.add(description)
                db.session.commit()
        else:
            return "Debes elegir o agregar una descripción."

        total_amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        local = request.form['local']
        payment_type_id = request.form['payment_type']

        # Crear el ticket con la descripción seleccionada o nueva
        ticket = Ticket(description=description, total_amount=total_amount, date=date, local=local, payment_type_id=payment_type_id)
        db.session.add(ticket)
        db.session.commit()

        # Procesar y agregar productos si existen
        products_data = request.form.get('products')
        if products_data:
            products = json.loads(products_data)
            for product in products:
                product_name = product['name']
                product_price = product['price']
                product_quantity = product['quantity']

                # Crear el producto y registrar el precio en ProductPrice
                new_product = Product(name=product_name, quantity=product_quantity, ticket_id=ticket.id)
                db.session.add(new_product)
                db.session.commit()

                product_price_entry = ProductPrice(date=date, price=product_price, product_id=new_product.id)
                db.session.add(product_price_entry)

        db.session.commit()
        return redirect(url_for('main.index'))

    payment_types = PaymentType.query.all()
    descriptions = Description.query.all()
    return render_template('add_expense.html', payment_types=payment_types, descriptions=descriptions)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/view_tickets')
def view_tickets():
    # Número de tickets a mostrar, configurable
    ticket_count = 10  # Puedes cambiar este número en el futuro según lo necesites

    # Consultar los últimos tickets
    tickets = Ticket.query.order_by(Ticket.date.desc()).limit(ticket_count).all()

    return render_template('view_tickets.html', tickets=tickets)
