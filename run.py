from app import create_app, db
from app.models import PaymentType, Description, Ticket, Product, ProductPrice
from datetime import datetime

app = create_app()

with app.app_context():
    # Crear las tablas en la base de datos
    db.create_all()

    # Cargar datos ficticios en PaymentType si la tabla está vacía
    if not PaymentType.query.first():
        payment_types = ['Efectivo', 'Tarjeta', 'Bizum', 'Transferencia', 'Paypal', 'Otros']
        for payment_type in payment_types:
            db.session.add(PaymentType(name=payment_type))

    # Cargar datos ficticios en Description si la tabla está vacía
    if not Description.query.first():
        descriptions = ['Ticket Lupa', 'Ticket Mercadona']
        for description in descriptions:
            db.session.add(Description(name=description))

    # Cargar datos ficticios en Ticket si la tabla está vacía
    if not Ticket.query.first():
        tickets = [
            Ticket(description_id=1, total_amount=2.54, date=datetime.strptime('2024-10-11', '%Y-%m-%d'), local='Lupa', payment_type_id=1),
            Ticket(description_id=2, total_amount=3.25, date=datetime.strptime('2024-10-11', '%Y-%m-%d'), local='Mercadona', payment_type_id=2)
        ]
        db.session.bulk_save_objects(tickets)

    # Cargar datos ficticios en Product si la tabla está vacía
    if not Product.query.first():
        products = [
            Product(id=1, name='Baguette', quantity=1, ticket_id=1),
            Product(id=2, name='Jeta', quantity=1, ticket_id=1),
            Product(id=3, name='Bizcocho', quantity=1, ticket_id=2)
        ]
        db.session.bulk_save_objects(products)

    # Cargar datos ficticios en ProductPrice si la tabla está vacía
    if not ProductPrice.query.first():
        product_prices = [
            ProductPrice(id=1, date=datetime.now().date(), price=0.34, product_id=1),
            ProductPrice(id=2, date=datetime.now().date(), price=2.20, product_id=2),
            ProductPrice(id=3, date=datetime.now().date(), price=3.25, product_id=3)
        ]
        db.session.bulk_save_objects(product_prices)

    # Confirmar todos los cambios en la base de datos
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
