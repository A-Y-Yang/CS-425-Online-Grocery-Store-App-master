from shop import db, login_manager

@login_manager.user_loader
def user_load(user_id):
    return User.query.get(user_id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
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
        return '<User %r>' % self.email

class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20), unique = False, nullable = False)
    last_name =  db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    salary = db.Column(db.Integer, unique = False, nullable = False)
    job_title =  db.Column(db.String(20), unique = False, nullable = False)
    address_line_one = db.Column(db.String(30), unique = False, nullable = False)
    address_line_two = db.Column(db.String(30), unique = False, nullable = True)
    address_city = db.Column(db.String(20), unique = False, nullable = False)
    address_state = db.Column(db.String(20), unique = False, nullable = False)
    address_zipcode = db.Column(db.String(5), unique = False, nullable = False)

    def __repr__(self):
        return '<Staff %r>' % self.email

class Supplier(db.Model):
    supplier_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    address_line_one = db.Column(db.String(30), unique = False, nullable = False)
    address_line_two = db.Column(db.String(30), unique = False, nullable = True)
    address_city = db.Column(db.String(20), unique = False, nullable = False)
    address_state = db.Column(db.String(20), unique = False, nullable = False)
    address_zipcode = db.Column(db.String(5), unique = False, nullable = False)

    def __repr__(self):
        return '<Supplier %r>' % self.email

class Warehouse(db.Model):
    warehouse_id= db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = False, nullable = False)
    address_line_one = db.Column(db.String(30), unique = False, nullable = False)
    address_line_two = db.Column(db.String(30), unique = False, nullable = True)
    address_city = db.Column(db.String(20), unique = False, nullable = False)
    address_state = db.Column(db.String(20), unique = False, nullable = False)
    address_zipcode = db.Column(db.String(5), unique = False, nullable = False)
    capacity = db.Column(db.Float, nullable = False)
    capacity_used = db.Column(db.Float, nullable = False, default = 0)
    capacity_remained = db.Column(db.Float, default = capacity)

    def __repr__(self):
        return '<Warehouse %r>' % self.name
        
db.create_all()