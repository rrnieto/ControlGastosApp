from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes, models
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

        # Inicializar datos para la tabla PaymentType si está vacía
        if not models.PaymentType.query.first():
            payment_types = ['Efectivo', 'Tarjeta', 'Bizum', 'Transferencia', 'Paypal', 'Otros']
            for payment_type in payment_types:
                db.session.add(models.PaymentType(name=payment_type))
            db.session.commit()

    return app
