from app import create_app, db
from app.models import PaymentType, Description, Ticket, Product, ProductTicket
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

    

    

  

    # Confirmar todos los cambios en la base de datos
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
