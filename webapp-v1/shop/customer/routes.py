from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, login_manager
from .forms import RegistrationForm, LoginForm, Checkout
from .models import Customer, Credit_Card
from shop.product.models import Product, Category
import os

@app.route('/')
def home():
    return "Server OK"

@app.route('/customer')
def customer():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Product.query.order_by(Product.name.asc()).all()
    return render_template('customer/index.html', title = 'Customer Page', products = products)
