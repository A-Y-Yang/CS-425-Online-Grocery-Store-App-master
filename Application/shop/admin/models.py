from shop import db, login_manager
from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Computed, CHAR

@login_manager.user_loader
def user_load(user_id):
    return User.query.get(user_id)

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, db.Sequence('customer_id_sq', start = 1000001, increment = 1, minvalue = 1000001, maxvalue = 1999999), primary_key = True)
    first_name = db.Column(db.String(20), unique = False, nullable = False)
    last_name =  db.Column(db.String(20), unique = False, nullable = False)
    phone = db.Column(db.CHAR(10), unique = False, nullable = True)
    email = db.Column(db.String(50), unique = True, nullable = False)
    payment_total = db.Column(db.Numeric(9,2), unique = False, default = 0)
    paid_total = db.Column(db.Numeric(9,2), unique = False, default = 0)
    balance = db.Column(db.Numeric(9,2), Computed('payment_total - paid_total'))
    da_line_one = db.Column(db.String(100), unique = False, nullable = False)
    da_line_two = db.Column(db.String(100), unique = False, nullable = True)
    da_city = db.Column(db.String(50), unique = False, nullable = False)
    da_state = db.Column(db.String(25), unique = False, nullable = False)
    da_zipcode = db.Column(db.CHAR(5), unique = False, nullable = False)
    
    __table_args__ = (CheckConstraint('payment_total >= 0'), CheckConstraint('paid_total >= 0'), CheckConstraint('balance >= 0'),)

    def __repr__(self):
        return '<Customer %r>' % self.email

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, db.Sequence('staff_id_sq', start = 2000001, increment = 1, minvalue = 2000001, maxvalue = 2999999), primary_key = True)
    first_name = db.Column(db.String(20), unique = False, nullable = False)
    last_name =  db.Column(db.String(20), unique = False, nullable = False)
    a_line_one = db.Column(db.String(100), unique = False, nullable = True)
    a_line_two = db.Column(db.String(100), unique = False, nullable = True)
    a_city = db.Column(db.String(50), unique = False, nullable = True)
    a_state = db.Column(db.String(25), unique = False, nullable = True)
    a_zipcode = db.Column(db.CHAR(5), unique = False, nullable = True)
    phone = db.Column(db.CHAR(10), unique = False, nullable = True)
    email = db.Column(db.String(50), unique = True, nullable = False)
    salary = db.Column(db.Integer, unique = False, nullable = False)
    job_title =  db.Column(db.String(20), unique = False, nullable = False)
    __table_args__ = (CheckConstraint('salary > 0'),)
    
    def __repr__(self):
        return '<Staff %r>' % self.email


class Supplier(db.Model):
    __tablename__ = 'supplier'
    supplier_id = db.Column(db.Integer, db.Sequence('supplier_id_sq', start = 8000001, increment = 1, minvalue = 8000001, maxvalue = 8999999), primary_key = True)
    name = db.Column(db.String(20), unique = False, nullable = False)
    phone = db.Column(db.CHAR(10), unique = False, nullable = True)
    email = db.Column(db.String(50), unique = True, nullable = False)
    a_line_one = db.Column(db.String(100), unique = False, nullable = False)
    a_line_two = db.Column(db.String(100), unique = False, nullable = True)
    a_city = db.Column(db.String(50), unique = False, nullable = False)
    a_state = db.Column(db.String(25), unique = False, nullable = False)
    a_zipcode = db.Column(db.CHAR(5), unique = False, nullable = False)

    def __repr__(self):
        return '<Supplier %r>' % self.email

class CreditCard(db.Model):
    __tablename__ = 'credit_card'
    card_number = db.Column(db.CHAR(16), primary_key = True)
    card_owner_name = db.Column(db.String(40), unique = False, nullable = False)
    card_expire_date = db.Column(db.CHAR(4), unique = False, nullable = False)
    card_cvv = db.Column(db.CHAR(3), unique = False, nullable = False)
    CBA_line_one = db.Column(db.String(100), unique = False, nullable = False)
    CBA_line_two = db.Column(db.String(100), unique = False, nullable = True)
    CBA_city = db.Column(db.String(50), unique = False, nullable = False)
    CBA_state = db.Column(db.String(25), unique = False, nullable = False)
    CBA_zipcode = db.Column(db.CHAR(5), unique = False, nullable = False)
    __table_args__ = (CheckConstraint("card_expire_date ~ '[0][1-9][2][0-9]|[1][12][2][0-9]'", name='card_expire_date_constraint'), CheckConstraint("card_cvv ~ '[0-9]{3}'", name='cvv_constraint'),)

    def __repr__(self):
        return '<CreditCard %r>' % self.card_number

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique = True)

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, db.Sequence('product_id_sq', start = 3000001, increment = 1, minvalue = 3000001, maxvalue = 4999999), primary_key = True)
    product_name = db.Column(db.String(30), nullable = False, unique = True)
    price = db.Column(db.Numeric(9,2), nullable = False, unique = False)
    size = db.Column(db.Numeric(12,5), nullable = False, unique = False)
    add_info = db.Column(db.String(150), nullable = False, unique = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    category = db.relationship(Category, backref=db.backref('categories', lazy = True))
    image = db.Column(db.String(150), nullable = True)

    def __repr__(self):
        return '<Product %r>' % self.product_name

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, db.Sequence('order_id_sq', start = 5000001, increment = 1, minvalue = 5000001, maxvalue = 6999999), primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable = False)
    payment_card_number = db.Column(db.CHAR(16), db.ForeignKey('credit_card.card_number'), nullable = False)
    ordering_total = db.Column(db.Numeric(9,2), nullable = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    status = db.Column(db.String(8), nullable = False, default = 'issued')
    __table_args__ = (CheckConstraint('ordering_total >= 0'), CheckConstraint("status in ('pending','issued','send','received')"),)

    def __repr__(self):
        return '<Orders %r>' % self.order_id

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    warehouse_id= db.Column(db.Integer, db.Sequence('warehouse_id_sq', start = 9000001, increment = 1, minvalue = 9000001, maxvalue = 9999999), primary_key = True)
    name = db.Column(db.String(20), unique = False, nullable = False)
    a_line_one = db.Column(db.String(100), unique = False, nullable = False)
    a_line_two = db.Column(db.String(100), unique = False, nullable = True)
    a_city = db.Column(db.String(50), unique = False, nullable = False)
    a_state = db.Column(db.String(25), unique = False, nullable = False)
    a_zipcode = db.Column(db.CHAR(5), unique = False, nullable = False)
    capacity = db.Column(db.Numeric(12,5), nullable = False)
    capacity_used = db.Column(db.Numeric(12,5), nullable = False, default = 0)
    capacity_remained = db.Column(db.Numeric(12,5), Computed('capacity - capacity_used'))
    __table_args__ = (CheckConstraint('capacity > 0'), CheckConstraint('capacity_used >= 0'), CheckConstraint('capacity_remained >= 0'),)

    def __repr__(self):
        return '<Warehouse %r>' % self.name

class SupplierItem(db.Model):
    __tablename__ = 'supplier_item'
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id', ondelete='CASCADE'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'), primary_key = True)
    supplier_price = db.Column(db.Numeric(9,2),  nullable = False)
    __table_args__ = (CheckConstraint('supplier_price > 0'),)

    def __repr__(self):
        return '<SupplierItem %r>' % self.supplier_id, self.product_id

class SupplyRequest(db.Model):
    __tablename__ = 'request'
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key = True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), primary_key = True)
    details = db.Column(db.String(100), primary_key = True)

class ProductPrice(db.Model):
    __tablename__ = 'product_price'
    product_id = db.Column(db.Integer, db.Sequence('product_id_sq', start = 3000001, increment = 1, minvalue = 3000001, maxvalue = 4999999), primary_key = True)
    delivery_state = db.Column(db.String(25), primary_key = True)
    price = db.Column(db.Integer, nullable = False, unique = False)

class Pricing(db.Model):
    __tablename__ = 'pricing'
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    product_id = db.Column(db.Integer, primary_key = True)
    delivery_state = db.Column(db.String(25), primary_key = True)
    new_price = db.Column(db.Numeric(9,2))
    __table_args__ = (ForeignKeyConstraint(['product_id','delivery_state'],['product_price.product_id','product_price.delivery_state']), CheckConstraint('new_price > 0'),)

class Stock(db.Model):
    __tablename__ = 'stock'
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'), primary_key = True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'), primary_key = True)
    item_quantity = db.Column(db.Integer, nullable = False)
    size_total = db.Column(db.Numeric(12,5), nullable = False)
    __table_args__ = (CheckConstraint('item_quantity > 0'), CheckConstraint('size_total > 0'),)

class AddStock(db.Model):
    __tablename__ = 'add_stock'
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    product_id = db.Column(db.Integer, primary_key = True)
    warehouse_id = db.Column(db.Integer, primary_key = True)
    add_quantity = db.Column(db.Integer, nullable = False)
    add_size = db.Column(db.Numeric(12,5), nullable = False)
    __table_args__ = (ForeignKeyConstraint(['product_id','warehouse_id'],['stock.product_id','stock.warehouse_id']), CheckConstraint('add_size > 0'), CheckConstraint('add_quantity > 0'),)

class Ordering(db.Model):
    __tablename__ = 'ordering'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key = True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key = True)

class Availability(db.Model):
    __tablename__ = 'availability'
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'), primary_key = True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id', ondelete='CASCADE'), primary_key = True)
    item_quantity = db.Column(db.Integer)
    __table_args__ = (CheckConstraint('item_quantity >=0'),)

class Owns(db.Model):
    __tablename__ = 'owns'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id', ondelete='CASCADE'), primary_key = True)
    card_number = db.Column(db.CHAR(16), db.ForeignKey('credit_card.card_number', ondelete='CASCADE'), primary_key = True)

class PaidWith(db.Model):
    __tablename__ = 'paidwith'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key = True)
    card_number = db.Column(db.CHAR(16), db.ForeignKey('credit_card.card_number'), primary_key = True)

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)
    unit_price = db.Column(db.Numeric(9,2), nullable = False)
    subtotal =  db.Column(db.Numeric(9,2), Computed('quantity * unit_price'))
    __table_args__ = (CheckConstraint('quantity > 0'), CheckConstraint('unit_price >= 0'), CheckConstraint('subtotal >= 0'),)

class Includes(db.Model):
    __tablename__ = 'includes'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)
    __table_args__ = (CheckConstraint('quantity > 0'),)

class Order_item_warehouse_id(db.Model):
    __tablename__ = 'order_item_warehouse_id'
    order_id = db.Column(db.Integer,db.ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'), primary_key = True)

class Stores(db.Model):
    __tablename__ = 'stores'
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'), primary_key = True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id', ondelete='CASCADE'), primary_key = True)
    size_total = db.Column(db.Numeric(12,5), nullable = False)

db.create_all()