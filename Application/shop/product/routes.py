from flask import render_template, request, redirect, url_for, flash, session, current_app
from shop import app, db, photos, login_manager
from flask_login import login_required, logout_user, current_user
from .models import Category, Product
from shop.customer.models import CustomerOrder, OrderItem
from shop.customer.forms import Checkout
from .forms import Addproduct
import os

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        db.seesion.commit()
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

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    form = Addproduct(request.form)
    if request.method == 'POST':
        image_1 = photos.save(request.files.get('image'))
        product = Product(name = form.name.data, price = form.price.data,
                    size = form.size.data, add_info = form.add_info.data, 
                    category_id = request.form.get('category'), image = image_1)
        db.session.add(product)
        db.session.commit()
        flash(f'{form.name.data} is added to your database.', 'success')
        return redirect(url_for('admin'))
    return render_template('product/addproduct.html', title = "Add Product Page", form = form, categories = categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    form = Addproduct(request.form)
    category = request.form.get('category')
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.size = form.size.data
        product.add_info = form.add_info.data
        product.category_id = category
        db.session.commit()
        flash(f'Your product {form.name.data} has been updated.', 'success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.size.data = product.size
    form.add_info.data = product.add_info
    category = product.category_id
    return render_template('product/updateproduct.html', title = "Update Product Page", form = form, categories = categories, product = product)

@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images" + product.image))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'Your product {product.name} was deleted.', 'success')
        return redirect(url_for('admin'))
    flash(f'Cannot delete the product.','danger')
    return render_template(url_for('admin'))

@app.route('/product_details/<int:id>', methods=['GET', 'POST'])
def product_details(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    product = Product.query.get_or_404(id)
    return render_template('product/product_details.html', product = product)

@app.route('/addorder', methods=['GET', 'POST'])
#@login_required
def addorder():
    if current_user.is_authenticated:
        customer_id = current_user.id
        try:
            form = Checkout(request.form)
            for key, product in session['Shoppingcart'].items():
                grandtotal += int(product['price'])*int(product['quantity'])
            order = CustomerOrder(customer_id = customer_id, payment_card_number = form.payment_card_number.data, order_grand_total = grandtotal)
            db.session.add(order)
            for key, product in session['Shoppingcart'].items():
                orderitem = OrderItem(order_id = order.order_id, customer_id = customer_id, quantity = product['quantity'], unit_price = product['unit_price'],subtotal = product['subtotal'])
                db.session.add(orderitem)
            flash(f'Your order has been issued', 'success')
            order.status = "issued"
            db.session.commit()
            return redirect(url_for('customer'))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order','danger')
            return redirect(url_for('getCart'))
            
            