from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from shop import app, db, login_manager
from .forms import RegistrationForm, LoginForm
from .models import User, Supplier, Warehouse, Staff
from shop.product.models import Product, Category
import os

@app.route('/')
def home():
    return "Server OK"

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Product.query.order_by(Product.name.asc()).all()
    return render_template('admin/index.html', title = 'Admin Page', products = products)

@app.route('/customer')
def customer():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Product.query.order_by(Product.name.asc()).all()
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
        user = User(first_name = form.first_name.data, last_name = form.last_name.data,
                    email = form.email.data, phone = form.phone.data, 
                    address_line_one= form.address_line_one.data, address_line_two = form.address_line_two.data,
                    address_city = form.address_city.data, address_state = form.address_state.data,
                    address_zipcode = form.address_zipcode.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.first_name.data}! Thanks for registering', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', title = 'Registeration User', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(first_name = form.first_name.data).first()
        staff = Staff.query.filter_by(first_name = form.first_name.data).first()
        if user and user.email == form.email.data:
            session['email'] = form.email.data
            flash(f'Welcome {form.first_name.data}. You are logged-in.', 'success')
            return redirect(request.args.get('next') or url_for('customer'))
        if staff and staff.email == form.email.data:
            session['email'] = form.email.data
            flash(f'Welcome {form.first_name.data}. You are logged-in.', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Wrong email. Please try again.', 'danger')
    return render_template('admin/login.html', title = 'Login Page', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/suppliers')
def suppliers():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    suppliers = Supplier.query.all()
    return render_template('admin/supplier.html', title = 'Supplier Page', suppliers = suppliers)

@app.route('/addsupplier', methods=['GET', 'POST'])
def addsupplier():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    form = Addsupplier(request.form)
    if request.method == 'POST':
        supplier = Supplier(name = form.name.data, email = form.email.data,
                    phone = form.phone.data, address_line_one = form.address_line_one.data, 
                    address_line_two = form.address_line_two.data, address_city = form.address_city.data, 
                    address_state = form.address_state.data, address_zipcode = form.address_zipcode.data)
        db.session.add(supplier)
        db.session.commit()
        flash(f'{form.name.data} is added to your database.', 'success')
        return redirect(url_for('admin'))
    return render_template('supplier/addsupplier.html', title = "Add Supplier Page", form = form, categories = categories)

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
        return redirect(url_for('admin'))
    flash(f'Cannot delete the supplier.','danger')
    return render_template(url_for('admin'))

@app.route('/warehouses')
def warehouses():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    warehouses = Warehouse.query.all()
    return render_template('admin/warehouse.html', title = 'Warehouse Page', warehouses = warehouses)

@app.route('/addwarehouse', methods=['GET', 'POST'])
def addwarehouse():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    form = Addwarehouse(request.form)
    if request.method == 'POST':
        
        warehouse = Warehouse(name = form.name.data, address_line_one = form.address_line_one.data, 
                    address_line_two = form.address_line_two.data, address_city = form.address_city.data, 
                    address_state = form.address_state.data, address_zipcode = form.address_zipcode.data,
                    capacity = form.capacity.data, capacity_used = form.capacity_used.data, 
                    capacity_remained = form.capacity_remained.data)
        db.session.add(warehouse)
        db.session.commit()
        flash(f'{form.name.data} is added to your database.', 'success')
        return redirect(url_for('admin'))
    return render_template('warehouse/addpWarehouse.html', title = "Add Warehouse Page", form = form, categories = categories)

@app.route('/updatewarehouse/<int:warehouse_id>', methods=['GET', 'POST'])
def updatewarehouse(warehouse_id):
    if 'email' not in session:
        flash(f'Plese login first','danger')
    updatewh = warehouse.query.get_or_404(warehouse_id)
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

