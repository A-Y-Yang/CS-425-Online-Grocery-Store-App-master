from flask import render_template, request, redirect, url_for, flash, session, current_app
from shop import app, db, photos, login_manager
from flask_login import login_required, logout_user, current_user
from shop.admin.models import Category, Product, Orders, OrderItem, Owns, Customer, Warehouse, Availability, Staff
from shop.customer.forms import Checkout
from .forms import Addproduct
from decimal import Decimal
import os
from shop.admin.models import Staff

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        db.session.commit()
        flash(f'The Category {getcategory} was added to your database.', 'success')
        return redirect(url_for('addcategory'))
    return render_template('product/addcategory.html', title = "Add Category")

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Plese login first','danger')
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecat.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('product/updatecat.html', title = "Update Category Page", updatecat = updatecat)

@app.route('/addproduct/<int:id>', methods=['GET', 'POST'])
def addproduct(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    try: 
        staff = Staff.query.get_or_404(id)
        categories = Category.query.all()
        form = Addproduct(request.form)
        if request.method == 'POST':
            image_1 = photos.save(request.files.get('image'))
            product = Product(product_name = form.product_name.data, price = form.price.data,
                        size = form.size.data, add_info = form.add_info.data, 
                        category_id = request.form.get('category'), image = image_1)
            db.session.add(product)
            db.session.commit()
            flash(f'{form.product_name.data} is added to your database.', 'success')
            return redirect(url_for('admin', id = id))
    except Exception as e:
        print(e)
        flash(f'Cannot add the product.','danger')
        return redirect(url_for('admin', id = id))
    return render_template('product/addproduct.html', title = "Add Product Page", staff = staff, form = form, categories = categories)

@app.route('/updateproduct/<int:id>/<int:product_id>', methods=['GET', 'POST'])
def updateproduct(id, product_id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('customer_login'))
    try:
        categories = Category.query.all()
        staff = Staff.query.get_or_404(id)
        product = Product.query.get_or_404(product_id)
        form = Addproduct(request.form)
        category = request.form.get('category')
        if request.method == 'POST':
            product.product_name = form.product_name.data
            product.price = form.price.data
            product.size = form.size.data
            product.add_info = form.add_info.data
            product.category_id = category
            db.session.commit()
            flash(f'Your product {form.product_name.data} has been updated.', 'success')
            return redirect(url_for('admin', id = id))
        form.product_name.data = product.product_name
        form.price.data = product.price
        form.size.data = product.size
        form.add_info.data = product.add_info
        category = product.category_id
    except Exception as e:
        print(e)
        flash(f'Cannot update the product.','danger')
        return redirect(url_for('admin', id = id))
    return render_template('product/updateproduct.html', title = "Update Product Page", staff = staff, form = form, categories = categories, product = product)

@app.route('/deleteproduct/<int:id>/<int:product_id>', methods=["POST"])
def deleteproduct(id, product_id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('customer_login'))
    try:
        staff = Staff.query.get_or_404(id)
        product = Product.query.get_or_404(product_id)
        if request.method == "POST":
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images" + product.image))
            except Exception as e:
                print(e)
            db.session.delete(product)
            db.session.commit()
            flash(f'Your product {product.product_name} was deleted.', 'success')
            return redirect(url_for('admin', id = id))
    except Exception as e:
        print(e)
        flash(f'Cannot delete the product.','danger')
        return redirect(url_for('admin', id = id))


@app.route('/product_details/<int:id>', methods=['GET', 'POST'])
def product_details(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    product = Product.query.get_or_404(id)
    return render_template('product/product_details.html', product = product)

@app.route('/addorder/<int:id>', methods=['GET', 'POST'])
def addorder(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    #if current_user.is_authenticated:
    try:
        form = Checkout(request.form)
        grandtotal = 0
        for key, product in session['Shoppingcart'].items():
            grandtotal += float(product['price'])*int(product['quantity'])
        order = Orders(customer_id = id, payment_card_number = form.payment_card_number.data, ordering_total = grandtotal)
        db.session.add(order)
        db.session.commit()
        for key, product in session['Shoppingcart'].items():
            orderitem = OrderItem(order_id = order.order_id, product_id = int(key),
                                quantity = product['quantity'], unit_price = product['price'])
            db.session.add(orderitem)
            customer = Customer.query.filter_by(customer_id = id).first()
            warehouse = Warehouse.query.filter_by(a_state = customer.da_state).first()
            reduceavailability = Availability.query.filter_by(product_id = int(key)).filter_by(warehouse_id = warehouse.warehouse_id).first()
            if (reduceavailability.item_quantity > int(orderitem.quantity)):
                reduceavailability.item_quantity -= int(orderitem.quantity)
                db.session.add(orderitem)
            else:
                db.session.delete(order)
                db.session.commit()
                flash(f'{product["name"]} is not available. Please review your order.', 'danger')
                return redirect(url_for('getCart', id = id))
        customer = Customer.query.get_or_404(id)
        customer.payment_total += Decimal(grandtotal)
        order.status = 'send'
        db.session.commit()
        flash(f'Your order has been issued', 'success')
        session.pop('Shoppingcart')
        return redirect(url_for('customer', id = id))
    except Exception as e:
        print(e)
        flash('Somethings went wrong while get order','danger')
        return redirect(url_for('getCart', id = id))
            
            