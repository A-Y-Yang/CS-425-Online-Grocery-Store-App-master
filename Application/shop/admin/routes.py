from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from decimal import Decimal
from shop import app, db, login_manager
from .forms import RegistrationForm, LoginForm, StaffRegistrationForm, Addsupplier, Addwarehouse
from .models import Customer, Staff, Supplier, Warehouse, Product, Category, Orders, CreditCard, Stock, AddStock, SupplierItem, ProductPrice, Availability
from .state import state_list
import os

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    products = Product.query.order_by(Product.product_name.asc()).all()
    return render_template('admin/index.html', title = 'Admin Page', products = products)

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/customer_list')
def customer_list():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    customers = Customer.query.all()
    return render_template('admin/customer_list.html', title = 'Customer List Page', customers = customers)

@app.route('/order_list', methods = ['GET', 'POST'])
def order_list():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    orders = Orders.query.all()
    if request.method == 'POST':
        updateorder = Orders.query.filter_by(order_id = request.form.get('order_id')).first()
        updateorder.status = 'received'
        customer = Customer.query.filter_by(customer_id = updateorder.customer_id).first()
        customer.paid_total += updateorder.ordering_total
        db.session.commit()
        flash(f'The order status is changed to "received".', 'success')
    return render_template('admin/order_list.html', title = 'Order List Page', orders = orders)

@app.route('/suppliers')
def suppliers():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    suppliers = Supplier.query.all()
    return render_template('admin/supplier.html', title = 'Supplier Page', suppliers = suppliers)

@app.route('/addsupplier', methods=['GET', 'POST'])
def addsupplier():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    form = Addsupplier(request.form)
    if request.method == 'POST':
        supplier = Supplier(name = form.name.data, phone = form.phone.data, email = form.email.data, 
                    a_line_one = form.a_line_one.data, a_line_two = form.a_line_two.data, a_city = form.a_city.data,
                    a_state = form.a_state.data, a_zipcode = form.a_zipcode.data)
        db.session.add(supplier)
        db.session.commit()
        flash(f'Supplier {form.name.data} is added to your database.', 'success')
        return redirect(url_for('suppliers'))
    return render_template('admin/addsupplier.html', title = "Add Supplier Page", form = form)

@app.route('/supplier_details/<int:id>', methods=['GET', 'POST'])
def supplier_details(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    supplier = Supplier.query.get_or_404(id)
    return render_template('supplier/supplier_details.html', supplier = supplier)

@app.route('/updatesupplier/<int:supplier_id>', methods=['GET', 'POST'])
def updatesupplier(supplier_id):
    if 'email' not in session:
        flash(f'Plese login first','danger')
    supplier = Supplier.query.get_or_404(supplier_id)
    form = Addsupplier(request.form)
    if request.method =="POST":
        supplier.name = form.name.data
        supplier.phone = form.phone.data
        supplier.email = form.email.data
        supplier.a_line_one = form.a_line_one.data
        supplier.a_line_two = form.a_line_two.data
        supplier.a_city = form.a_city.data
        supplier.a_state = form.a_state.data
        supplier.a_zipcode = form.a_zipcode.data
        flash(f'This Supplier {form.name.data} has been updated', 'success')
        db.session.commit()
        return redirect(url_for('suppliers'))
    form.name.data = supplier.name
    form.phone.data = supplier.phone
    form.email.data = supplier.email
    form.a_line_one.data = supplier.a_line_one
    form.a_line_two.data = supplier.a_line_two
    form.a_city.data = supplier.a_city
    form.a_state.data = supplier.a_state
    form.a_zipcode.data = supplier.a_zipcode
    return render_template('admin/updatesupplier.html', title = "Update Supplier Page", form = form, supplier=supplier)

@app.route('/deletesupplier/<int:supplier_id>', methods=["POST"])
def deletesupplier(supplier_id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    supplier = Supplier.query.get_or_404(supplier_id)
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
        return redirect(url_for('home'))
    warehouses = Warehouse.query.all()
    return render_template('admin/warehouse.html', title = 'Warehouse Page', warehouses = warehouses)

@app.route('/addwarehouse', methods=['GET', 'POST'])
def addwarehouse():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    form = Addwarehouse(request.form)
    if request.method == 'POST':
        warehouse = Warehouse(name = form.name.data, a_line_one = form.a_line_one.data,
                    a_line_two = form.a_line_two.data, a_city = form.a_city.data,
                    a_state = form.a_state.data, a_zipcode = form.a_zipcode.data,
                    capacity = form.capacity.data)
        db.session.add(warehouse)
        db.session.commit()
        flash(f'Warehouse {form.name.data} is added to your database.', 'success')
        return redirect(url_for('warehouses'))
    return render_template('admin/addwarehouse.html', title = "Add Warehouse Page", form = form)

@app.route('/warehouse_details/<int:id>', methods=['GET', 'POST'])
def warehouse_details(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    warehouse = Warehouse.query.get_or_404(id)
    return render_template('warehouse/warehouse_details.html', warehouse = warehouse)

@app.route('/updatewarehouse/<int:warehouse_id>', methods=['GET', 'POST'])
def updatewarehouse(warehouse_id):
    if 'email' not in session:
        flash(f'Plese login first','danger')
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    form = Addwarehouse(request.form)
    if request.method =="POST":
        warehouse.name = form.name.data
        warehouse.a_line_one = form.a_line_one.data
        warehouse.a_line_two = form.a_line_two.data
        warehouse.a_city = form.a_city.data
        warehouse.a_state = form.a_state.data
        warehouse.a_zipcode = form.a_zipcode.data
        warehouse.capacity = form.capacity.data
        flash(f'This warehouse {form.name.data} has been updated', 'success')
        db.session.commit()
        return redirect(url_for('warehouses'))
    form.name.data = warehouse.name
    form.a_line_one.data = warehouse.a_line_one 
    form.a_line_two.data = warehouse.a_line_two
    form.a_city.data = warehouse.a_city
    form.a_state.data = warehouse.a_state
    form.a_zipcode.data = warehouse.a_zipcode
    form.capacity.data = warehouse.capacity
    return render_template('admin/updatewarehouse.html', title = "Update Warehouse Page", form = form, warehouse = warehouse)

@app.route('/deletewarehouse/<int:warehouse_id>', methods=["POST"])
def deletewarehouse(warehouse_id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    if request.method == "POST":
        db.session.delete(warehouse)
        db.session.commit()
        flash(f'This warehouse {warehouse.name} was deleted.', 'success')
        return redirect(url_for('admin'))
    flash(f'Cannot delete the warehouse.','danger')
    return render_template(url_for('admin'))

@app.route('/addstock', methods = ['GET', 'POST'])
def addstock():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    #staff = Staff.query.get_or_404(id)
    try: 
        warehouses = Warehouse.query.all()
        products = Product.query.all()
        if request.method == "POST":
            stock = request.form.get('product_id')
            quantity = request.form.get('quantity')
            product = Product.query.filter_by(product_id = stock).first()
            addstock = AddStock(staff_id = request.form.get('staff_id'), product_id = request.form.get('product_id'),
                                warehouse_id = request.form.get('warehouse_id'), add_quantity = quantity,
                                add_size = int(quantity)*float(product.size))
            if (Stock.query.filter_by(product_id = addstock.product_id).filter_by(warehouse_id = addstock.warehouse_id).first() is None):
                newstock = Stock(product_id = addstock.product_id, warehouse_id = addstock.warehouse_id, 
                                item_quantity = quantity, size_total = int(quantity)*float(product.size))
                db.session.add(newstock)
                db.session.add(addstock)
                updatewh = Warehouse.query.get_or_404(addstock.warehouse_id)
                updatewh.capacity_used += Decimal(addstock.add_size)
                updateavail = Availability.query.filter_by(product_id = addstock.product_id).filter_by(warehouse_id = addstock.warehouse_id)
                updateavail.item_quantity += int(quantity)
                db.session.commit()
                flash(f'New item {product.product_name} is added into Stock.', 'success')
            elif (AddStock.query.filter_by(product_id = addstock.product_id).filter_by(warehouse_id = addstock.warehouse_id).first() is None):
                db.session.add(addstock)
                updatestock = Stock.query.filter_by(product_id = addstock.product_id).filter_by(warehouse_id = addstock.warehouse_id).first()
                updatestock.item_quantity += int(addstock.add_quantity)
                updatewh = Warehouse.query.get_or_404(addstock.warehouse_id)
                updatewh.capacity_used += Decimal(addstock.add_size)
                updateavail = Availability.query.filter_by(product_id = addstock.product_id).filter_by(warehouse_id = addstock.warehouse_id)
                updateavail.item_quantity += int(quantity)
                db.session.commit()
                flash(f'New stock of {product.product_name} is added.', 'success')
            else:
                updatestock = Stock.query.filter_by(product_id = addstock.product_id).filter_by(warehouse_id = addstock.warehouse_id).first()
                updatestock.item_quantity += int(addstock.add_quantity)
                updatestock.size_total += Decimal(addstock.add_size)
                updatewh = Warehouse.query.get_or_404(addstock.warehouse_id)
                updatewh.capacity_used += Decimal(addstock.add_size)
                updateavail = Availability.query.filter_by(product_id = addstock.product_id).filter_by(warehouse_id = addstock.warehouse_id)
                updateavail.item_quantity += int(quantity)
                db.session.commit()
                flash(f'More stock {product.product_name} is added.', 'success')
    except Exception as e:
        print(e)
        flash(f'Somethings went wrong while get order','danger')
        return redirect(url_for('addstock'))
    return render_template('admin/addstock.html', title = "Add Stock Page", warehouses = warehouses, products = products)

@app.route('/supplierprice', methods = ['GET', 'POST'])
def supplierprice():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    suppliers = Supplier.query.all()
    products = Product.query.all()
    if request.method == "POST":
        newprice = SupplierItem(supplier_id = request.form.get('supplier_id'),product_id = request.form.get('product_id'),
                                supplier_price = request.form.get('newprice'))
        if (SupplierItem.query.filter_by(supplier_id = newprice.supplier_id).filter_by(product_id = newprice.product_id).first() is None):
            db.session.add(newprice)
            db.session.commit()
        else:
            updateprice = SupplierItem.query.filter_by(supplier_id = newprice.supplier_id).filter_by(product_id = newprice.product_id).first()
            updateprice.supplier_price = newprice.supplier_price
            db.session.commit()
        flash(f'New price is updated.', 'success')
    return render_template('admin/supplier_newprice.html', title = "Supplier Price Page", suppliers = suppliers, products = products)


@app.route('/pricebystate', methods = ['GET', 'POST'])
def stateprice():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    products = Product.query.all()
    states = state_list
    if request.method == "POST":
        stateprice = ProductPrice(product_id = request.form.get('product_id'),delivery_state = request.form.get('state'),
                                price = request.form.get('newprice'))
        if (stateprice.price == '0'):
            if (ProductPrice.query.filter_by(product_id = stateprice.product_id).filter_by(delivery_state = stateprice.delivery_state).first() is not None):
                deleteprice = ProductPrice.query.filter_by(product_id = stateprice.product_id).filter_by(delivery_state = stateprice.delivery_state).first()
                db.session.delete(deleteprice)
                db.session.commit()
                flash(f'This price record is deleted.', 'success')
            return render_template('admin/stateprice.html', title = "State Price Page", states = states, products = products)
        elif (ProductPrice.query.filter_by(product_id = stateprice.product_id).filter_by(delivery_state = stateprice.delivery_state).first() is None):
            db.session.add(stateprice)
            db.session.commit()
        else:
            updateprice = ProductPrice.query.filter_by(product_id = stateprice.product_id).filter_by(delivery_state = stateprice.delivery_state).first()
            updateprice.price = stateprice.price
            db.session.commit()
        flash(f'New price is updated.', 'success')
    return render_template('admin/stateprice.html', title = "State Price Page", states = states, products = products)