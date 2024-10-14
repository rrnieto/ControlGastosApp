from app import create_app, db
from app.models import PaymentType

app = create_app()

with app.app_context():
    db.create_all()
    
    # Población inicial de tipos de pago
    payment_types = ['Efectivo', 'Tarjeta', 'Bizum', 'Transferencia', 'Paypal', 'Otros']
    for payment_type in payment_types:
        if not PaymentType.query.filter_by(name=payment_type).first():
            db.session.add(PaymentType(name=payment_type))
    
    db.session.commit()
