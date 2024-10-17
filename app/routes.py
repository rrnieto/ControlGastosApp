from flask import Flask, Blueprint, render_template, request, redirect, url_for, Response
import io
import base64
from .models import Ticket, Product, ProductTicket, PaymentType, Description
from . import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MultipleLocator
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
    # Obtener el producto y el historial de compras completo
    product = Product.query.get_or_404(product_id)
    price_history = ProductTicket.query.filter_by(product_id=product_id).order_by(ProductTicket.date.desc()).all()

    # Filtrar el historial para mostrar solo cambios de precio
    filtered_history = []
    
    for i in range(len(price_history)):
        current_record = price_history[i]
        next_record = price_history[i+1] if i+1 < len(price_history) else None

        # Solo añadimos el registro si es el último con un precio constante antes de un cambio, o si es el último registro
        if (next_record and current_record.price != next_record.price) or not next_record:
            filtered_history.append(current_record)

    # Calcular el precio más bajo y el más alto
    lowest_price_record = ProductTicket.query.filter_by(product_id=product_id).order_by(ProductTicket.price.asc()).first()
    highest_price_record = ProductTicket.query.filter_by(product_id=product_id).order_by(ProductTicket.price.desc()).first()
    
    # Definir last_ticket_id como el ticket del último elemento en filtered_history
    last_ticket_id = filtered_history[-1].ticket_id if filtered_history else None

    # Preparar datos para el gráfico, usando solo las fechas y precios de filtered_history
    dates = [record.date for record in filtered_history]
    prices = [record.price for record in filtered_history]

    fig = Figure()
    ax = fig.subplots()
    ax.plot(dates, prices, marker='o', color='b')    
    #ax.set_xlabel('Fecha')
    #ax.set_ylabel('Precio (€)')
    ax.grid(True)

    # Formato de fecha personalizado en el eje X y establecer ticks específicos
    date_format = DateFormatter("%d/%m/%y")
    ax.xaxis.set_major_formatter(date_format)
    ax.set_xticks(dates)  # Solo mostrar fechas con cambios de precio
    fig.autofmt_xdate()  # Rotar las fechas para mejor visualización

    # Ajustar el eje Y para incrementos de 0.05 euros
    ax.yaxis.set_major_locator(MultipleLocator(0.05))

    # Convertir gráfico a imagen para mostrar en el HTML
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template(
        'product_history.html',
        product=product,
        price_history=filtered_history,
        lowest_price_record=lowest_price_record,
        highest_price_record=highest_price_record,
        last_ticket_id=last_ticket_id,
        plot_url=plot_url
    )


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/view_tickets')
def view_tickets():
    # Número de tickets a mostrar
    ticket_count = 10
    # Consultar los últimos tickets
    tickets = Ticket.query.order_by(Ticket.date.desc()).limit(ticket_count).all()
    return render_template('view_tickets.html', tickets=tickets)


@bp.route('/ticket_detail/<int:ticket_id>')
def ticket_detail(ticket_id):
    # Consulta el ticket y usa la tabla intermedia ProductTicket para obtener los productos
    ticket = Ticket.query.get_or_404(ticket_id)
    product_tickets = ProductTicket.query.filter_by(ticket_id=ticket_id).all()
    return render_template('ticket_detail.html', ticket=ticket, product_tickets=product_tickets)




