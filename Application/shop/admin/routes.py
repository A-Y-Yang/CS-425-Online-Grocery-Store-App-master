from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from shop import app, db, login_manager
from .forms import RegistrationForm, LoginForm, StaffRegistrationForm
from .models import Customer, Staff, Supplier, Warehouse, Product, Category, Orders
import os

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Product.query.order_by(Product.product_name.asc()).all()
    return render_template('admin/index.html', title = 'Admin Page', products = products)

@app.route('/customer')
def customer():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Product.query.order_by(Product.product_name.asc()).all()
    return render_template('customer/index.html', title = 'Customer Page', products = products)

@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    return render_template('admin/category.html', title = 'Category Page', categories = categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        customer = Customer(first_name = form.first_name.data, last_name = form.last_name.data,
                    phone = form.phone.data, email = form.email.data, 
                    da_line_one= form.da_line_one.data, da_line_two = form.da_line_two.data,
                    da_city = form.da_city.data, da_state = form.da_state.data,
                    da_zipcode = form.da_zipcode.data)
        db.session.add(customer)
        db.session.commit()
        flash(f'Welcome {form.first_name.data}! Thanks for registering', 'success')
        return redirect(url_for('customer_login'))
    return render_template('customer/register.html', title = 'Customer Registeration', form=form)

@app.route('/staff_register', methods=['GET', 'POST'])
def staff_register():
    form = StaffRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        staff = Staff(first_name = form.first_name.data, last_name = form.last_name.data,
                    a_line_one= form.a_line_one.data, a_line_two = form.a_line_two.data,
                    a_city = form.a_city.data, a_state = form.a_state.data,
                    a_zipcode = form.a_zipcode.data, phone = form.phone.data, email = form.email.data, 
                    salary = form.salary.data, job_title = form.job_title.data)
        db.session.add(staff)
        db.session.commit()
        flash(f'Welcome {form.first_name.data}! Your staff account is created', 'success')
        return redirect(url_for('staff_login'))
    return render_template('admin/register.html', title = 'Staff Registeration', form=form)

@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        staff = Staff.query.filter_by(first_name = form.first_name.data).first()
        if staff and staff.email == form.email.data:
            session['email'] = form.email.data
            flash(f'Welcome {form.first_name.data}. You are logged-in.', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Wrong email. Please try again.', 'danger')
    return render_template('admin/login.html', title = 'Staff Login Page', form=form)

@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        customer = Customer.query.filter_by(first_name = form.first_name.data).first()
        if customer and customer.email == form.email.data:
            session['email'] = form.email.data
            flash(f'Welcome {form.first_name.data}. You are logged-in.', 'success')
            return redirect(request.args.get('next') or url_for('customer'))
        else:
            flash(f'Wrong email. Please try again.', 'danger')
    return render_template('customer/login.html', title = 'Customer Login Page', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/customer_list')
def customer_list():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    customers = Customer.query.all()
    return render_template('admin/customer_list.html', title = 'Customer List Page', customers = customers)

@app.route('/order_list')
def order_list():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    orders = Orders.query.all()
    return render_template('admin/order_list.html', title = 'Order List Page', orders = orders)

@app.route('/suppliers')
def suppliers():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    suppliers = Supplier.query.all()
    return render_template('admin/supplier.html', title = 'Supplier Page', suppliers = suppliers)

@app.route('/updatesupplier/<int:supplier_id>', methods=['GET', 'POST'])
def updatesupplier(supplier_id):
    if 'email' not in session:
        flash(f'Plese login first','danger')
    updatesup = Supplier.query.get_or_404(supplier_id)
    supplier = request.form.get('supplier')
    if request.method =="POST":
        updatesup.name = supplier
        flash(f'This supplier {supplier} has been updated', 'success')
        db.session.commit()
        return redirect(url_for('suppliers'))
    return render_template('product/updatesupplier.html', title = "Update Supplier Page", updatesup = updatesup)

@app.route('/deletesupplier/<int:supplier_id>', methods=["POST"])
def deletesupplier(supplier_id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    supplier = request.form.get('supplier')
    if request.method == "POST":
        db.session.delete(supplier)
        db.session.commit()
        flash(f'This supplier {supplier.name} was deleted.', 'success')
        return redirect(url_for('suppliers'))
    flash(f'Cannot delete the supplier.','danger')
    return render_template(url_for('suppliers'))


@app.route('/warehouses')
def warehouses():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    warehouses = Warehouse.query.all()
    return render_template('admin/warehouse.html', title = 'Warehouse Page', warehouses = warehouses)

@app.route('/updatewarehouse/<int:warehouse_id>', methods=['GET', 'POST'])
def updatewarehouse(warehouse_id):
    if 'email' not in session:
        flash(f'Plese login first','danger')
    updatewh = Warehouse.query.get_or_404(warehouse_id)
    warehouse = request.form.get('warehouse')
    if request.method =="POST":
        updatewh.name = warehouse
        flash(f'This warehouse {warehouse} has been updated', 'success')
        db.session.commit()
        return redirect(url_for('warehouses'))
    return render_template('product/updatewarehouse.html', title = "Update Warehouse Page", updatesup = updatesup)

@app.route('/deletewarehouse/<int:warehouse_id>', methods=["POST"])
def deletewarehouse(warehouse_id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    warehouse = request.form.get('warehouse')
    if request.method == "POST":
        db.session.delete(warehouse)
        db.session.commit()
        flash(f'This warehouse {warehouse.name} was deleted.', 'success')
        return redirect(url_for('admin'))
    flash(f'Cannot delete the warehouse.','danger')
    return render_template(url_for('admin'))

