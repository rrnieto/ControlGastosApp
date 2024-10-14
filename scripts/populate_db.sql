-- Creación de datos ficticios para la tabla PaymentType
INSERT INTO payment_type (name) VALUES ('Efectivo');
INSERT INTO payment_type (name) VALUES ('Tarjeta');
INSERT INTO payment_type (name) VALUES ('Bizum');
INSERT INTO payment_type (name) VALUES ('Transferencia');
INSERT INTO payment_type (name) VALUES ('Paypal');
INSERT INTO payment_type (name) VALUES ('Otros');

-- Creación de datos ficticios para la tabla Description
INSERT INTO description (name) VALUES ('Ticket Lupa');
INSERT INTO description (name) VALUES ('Ticket Mercadona');

-- Creación de datos ficticios para la tabla Ticket
INSERT INTO ticket (id, description_id, total_amount, date, local, payment_type_id) 
VALUES (1, 1, 2.54, '2024-10-11', 'Lupa', 1);
INSERT INTO ticket (id, description_id, total_amount, date, local, payment_type_id) 
VALUES (2, 2, 3.25, '2024-10-11', 'Mercadona', 2);

-- Creación de datos ficticios para la tabla Product
INSERT INTO product (id, name, quantity, ticket_id) VALUES (1, 'Baguette', 1, 1);
INSERT INTO product (id, name, quantity, ticket_id) VALUES (2, 'Jeta', 1, 1);
INSERT INTO product (id, name, quantity, ticket_id) VALUES (3, 'Bizcocho', 1, 2);

-- Creación de datos ficticios para la tabla ProductPrice
INSERT INTO product_price (id, date, price, product_id) VALUES (1, date('now'), 0.34, 1);
INSERT INTO product_price (id, date, price, product_id) VALUES (2, date('now'), 2.20, 2);
INSERT INTO product_price (id, date, price, product_id) VALUES (3, date('now'), 3.25, 3);
