from shop import db
from datetime import datetime

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20), unique = False, nullable = False)
    last_name =  db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    payment_total = db.Column(db.Float, unique = False, default = 0)
    paid_total = db.Column(db.Float, unique = False, default = 0)
    balance = db.Column(db.Float, unique = False, default = 0)
    address_line_one = db.Column(db.String(30), unique = False, nullable = False)
    address_line_two = db.Column(db.String(30), unique = False, nullable = True)
    address_city = db.Column(db.String(20), unique = False, nullable = False)
    address_state = db.Column(db.String(20), unique = False, nullable = False)
    address_zipcode = db.Column(db.String(5), unique = False, nullable = False)

    def __repr__(self):
        return '<Customer %r>' % self.email
        
class CreditCard(db.Model):
    card_number = db.Column(db.String(16), primary_key = True)
    card_holder_name = db.Column(db.String(20), unique = False, nullable = False)
    card_expire_date = db.Column(db.String(4), unique = False, nullable = False)
    card_cvv = db.Column(db.Numeric(3,0), unique = False, nullable = False)
    CBA_line_one = db.Column(db.String(30), unique = False, nullable = False)
    CBA_line_two = db.Column(db.String(30), unique = False, nullable = True)
    CBA_city = db.Column(db.String(20), unique = False, nullable = False)
    CBA_state = db.Column(db.String(20), unique = False, nullable = False)
    CBA_zipcode = db.Column(db.String(5), unique = False, nullable = False)

    def __repr__(self):
        return '<Credit_Card %r>' % self.card_number

class CustomerOrder(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    payment_card_number = db.Column(db.String(16), nullable = False)
    order_grand_total = db.Column(db.Float, nullable = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    status = db.Column(db.String(10), default = "Pending", nullable = False)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.order_id

class OrderItem(db.Model):
    order_id = db.Column(db.Integer,primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)
    unit_price = db.Column(db.Integer, nullable = False)
    subtotal =  db.Column(db.Integer, nullable = False)

class OrderItemWarehouse(db.Model):
    order_id = db.Column(db.Integer,primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key = True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'), primary_key = True)

db.create_all()



