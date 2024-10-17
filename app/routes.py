from flask import Blueprint, render_template, request, redirect, url_for
from .models import Ticket, Product, ProductTicket, PaymentType, Description
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

        # Crear el ticket
        ticket = Ticket(description=description, total_amount=total_amount, date=date, local=local, payment_type_id=payment_type_id)
        db.session.add(ticket)
        db.session.commit()

        # Procesar y asociar productos con el ticket
        products_data = request.form.get('products')
        if products_data:
            products = json.loads(products_data)
            for product in products:
                product_name = product['name']
                product_price = product['price']
                product_quantity = product['quantity']

                # Comprobar si el producto ya existe, si no, crearlo
                existing_product = Product.query.filter_by(name=product_name).first()
                if not existing_product:
                    existing_product = Product(name=product_name)
                    db.session.add(existing_product)
                    db.session.commit()

                # Crear una entrada en ProductTicket para cada compra
                product_ticket_entry = ProductTicket(
                    product_id=existing_product.id,
                    ticket_id=ticket.id,
                    quantity=product_quantity,
                    price=product_price,
                    date=date
                )
                db.session.add(product_ticket_entry)

        db.session.commit()
        return redirect(url_for('main.index'))

    payment_types = PaymentType.query.all()
    descriptions = Description.query.all()
    return render_template('add_expense.html', payment_types=payment_types, descriptions=descriptions)

@bp.route('/product_history/<int:product_id>')
def product_history(product_id):
    # Obtener el producto y su historial de compras
    product = Product.query.get_or_404(product_id)
    price_history = ProductTicket.query.filter_by(product_id=product_id).order_by(ProductTicket.date.desc()).all()

    # Calcular el precio más bajo y el más alto
    lowest_price_record = ProductTicket.query.filter_by(product_id=product_id).order_by(ProductTicket.price.asc()).first()
    highest_price_record = ProductTicket.query.filter_by(product_id=product_id).order_by(ProductTicket.price.desc()).first()
    
    # Usar el ticket_id del registro de historial más reciente para el enlace de retorno
    last_ticket_id = price_history[0].ticket_id if price_history else None

    return render_template(
        'product_history.html',
        product=product,
        price_history=price_history,
        lowest_price_record=lowest_price_record,
        highest_price_record=highest_price_record,
        last_ticket_id=last_ticket_id
    )



@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/view_tickets')
def view_tickets():
    # Número de tickets a mostrar
    ticket_count = 3
    # Consultar los últimos tickets
    tickets = Ticket.query.order_by(Ticket.date.desc()).limit(ticket_count).all()
    return render_template('view_tickets.html', tickets=tickets)


@bp.route('/ticket_detail/<int:ticket_id>')
def ticket_detail(ticket_id):
    # Consulta el ticket y usa la tabla intermedia ProductTicket para obtener los productos
    ticket = Ticket.query.get_or_404(ticket_id)
    product_tickets = ProductTicket.query.filter_by(ticket_id=ticket_id).all()
    return render_template('ticket_detail.html', ticket=ticket, product_tickets=product_tickets)




