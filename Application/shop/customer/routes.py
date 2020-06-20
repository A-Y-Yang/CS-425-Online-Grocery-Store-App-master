from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from shop import app, db, login_manager
from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import Customer, Product, Category, Orders, CreditCard, Owns, Product, OrderItem
from .forms import AddcardForm, Checkout
import os

@app.route('/customer/<int:id>')
def customer(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    products = Product.query.order_by(Product.product_name.desc()).all()
    customer = Customer.query.get_or_404(id)
    return render_template('customer/index.html', title = 'Customer Page', products = products, customer = customer)

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

@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        customer = Customer.query.filter_by(first_name = form.first_name.data).first()
        if customer and customer.email == form.email.data:
            session['email'] = form.email.data
            flash(f'Welcome {form.first_name.data}. You are logged-in.', 'success')
            return redirect(request.args.get('next') or url_for('customer', id = customer.customer_id))
        else:
            flash(f'Wrong email. Please try again.', 'danger')
    return render_template('customer/login.html', title = 'Customer Login Page', form=form)

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    customer = Customer.query.get_or_404(id)
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        customer = Customer(first_name = form.first_name.data, last_name = form.last_name.data,
                    phone = form.phone.data, email = form.email.data, 
                    da_line_one= form.da_line_one.data, 
                    da_line_two = form.da_line_two.data,
                    da_city = form.da_city.data, da_state = form.da_state.data,
                    da_zipcode = form.da_zipcode.data)
        db.session.commit()
        flash(f'Your profile has been updated.', 'success')
        return redirect({{url_for('customer', id = customer.customer_id)}})
    form.first_name.data = customer.first_name
    form.last_name.data = customer.last_name
    form.phone.data = customer.phone
    form.email.data = customer.email
    form.da_line_one.data = customer.da_line_one
    form.da_line_two.data = customer.da_line_two
    form.da_city.data = customer.da_city
    form.da_state.data = customer.da_state
    form.da_zipcode.data = customer.da_zipcode
    return render_template('customer/profile.html', title = "Profile Page", form = form, customer = customer)

@app.route('/orders/<int:id>', methods = ['GET'])
def order_history(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    customer = Customer.query.get_or_404(id)
    orders = Orders.query.filter_by(customer_id = id).all()
    return render_template('customer/orders.html', title = 'Order History Page', orders = orders, customer = customer)

@app.route('/orders/<int:id>/<int:order_id>', methods = ['GET'])
def order_history_details(id, order_id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    customer = Customer.query.get_or_404(id)
    order = Orders.query.filter_by(order_id = order_id).first()
    products = db.session.query(Product.product_id,Product.product_name,Product.price,Product.image,OrderItem.quantity, OrderItem.subtotal).filter(OrderItem.order_id == order_id, Product.product_id == OrderItem.product_id)
    return render_template('customer/order_history.html', title = 'Order Details Page', order = order, products = products, customer = customer)

@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    categories = Category.query.all()
    return render_template('admin/category.html', title = 'Category Page', categories = categories)

@app.route('/addcards/<int:id>', methods=['GET', 'POST'])
def addcards(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    customer = Customer.query.get_or_404(id)
    form = AddcardForm(request.form)
    if request.method == 'POST' and form.validate():
        creditcard = CreditCard(card_number = form.card_number.data, card_owner_name = form.card_owner_name.data,
                    card_expire_date = form.card_expire_date.data, card_cvv = form.card_cvv.data, 
                    CBA_line_one = form.CBA_line_one.data, CBA_line_two = form.CBA_line_two.data, 
                    CBA_city = form.CBA_city.data, CBA_state = form.CBA_state.data, 
                    CBA_zipcode = form.CBA_zipcode.data)
        db.session.add(creditcard)
        db.session.commit()
        card_owner = Owns(customer_id = customer.customer_id, card_number = creditcard.card_number)
        db.session.add(card_owner)
        db.session.commit()
        flash(f'A new credit card is added to your database.', 'success')
        return redirect(url_for('customer', id = customer.customer_id))
    return render_template('customer/addcards.html', title = "Add Card Page", form = form, customer = customer)

@app.route('/creditcards/<int:id>', methods=['GET', 'POST'])
def creditcards(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    customer = Customer.query.get_or_404(id)
    customer_cards = db.session.query(Owns.card_number).filter(Owns.customer_id == id).subquery()
    creditcards = db.session.query(CreditCard).filter(CreditCard.card_number.in_(customer_cards))
    return render_template('customer/creditcards.html', title = 'Credit Card Page', creditcards = creditcards, customer = customer)

@app.route('/updatecards/<int:id>/<int:card_number>', methods=['GET', 'POST'])
def updatecards(id, card_number):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('home'))
    customer = Customer.query.get_or_404(id)
    creditcard = CreditCard.query.get_or_404(str(card_number))
    form = AddcardForm(request.form)
    if request.method == 'POST':
        creditcard = CreditCard(card_expire_date=form.card_expire_date.data, card_cvv=form.card_cvv.data,
                    CBA_line_one= form.CBA_line_one.data, CBA_line_two = form.CBA_line_two.data,
                    CBA_city = form.CBA_city.data, CBA_state = form.CBA_state.data,
                    CBA_zipcode = form.CBA_zipcode.data)
        db.session.commit()
        flash(f'Your credit card info has been updated.','success')
        return redirect(url_for('customer', id = customer.customer_id))
    form.card_number.data = creditcard.card_number
    form.card_owner_name.data = creditcard.card_owner_name
    form.card_expire_date.data = creditcard.card_expire_date
    form.card_cvv.data = creditcard.card_cvv
    form.CBA_line_one.data = creditcard.CBA_line_one
    form.CBA_line_two.data = creditcard.CBA_line_two
    form.CBA_city.data = creditcard.CBA_city
    form.CBA_state.data = creditcard.CBA_state
    form.CBA_zipcode.data = creditcard.CBA_zipcode
    return render_template('customer/updatecards.html', title = "Update Credit Cards", form = form, creditcard=creditcard, customer = customer)

@app.route('/deletecards/<int:id>/<int:card_number>', methods=["POST"])
def deletecards(id, card_number):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('customer_login'))
    customer = Customer.query.get_or_404(id)
    creditcard = CreditCard.query.get_or_404(str(card_number))
    card_owner = Owns.query.get_or_404([id,str(card_number)])
    if request.method == "POST":
        #try:
        #    os.unlink(os.path.join(current_app.root_path))
        #except Exception as e:
        #    print(e)
        db.session.delete(card_owner)
        db.session.delete(creditcard)
        db.session.commit()
        flash(f'Your credit card {creditcard.card_number} was deleted.', 'success')
        return redirect(url_for('customer', id = customer.customer_id))
    flash(f'Cannot delete the card.','danger')
    return render_template(url_for('customer', id = customer.customer_id))