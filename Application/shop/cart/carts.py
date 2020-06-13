from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import app, db
from shop.product.models import Product

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods = ['GET', 'POST'])
def addcart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price': product.price, 'quantity': quantity, 'image': product.image}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart']:
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else: 
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print (e)  
    finally:
        return redirect(request.referrer)

@app.route('/cart')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        flash(f'Cart is empty. Please add item(s).', 'danger')
        return redirect(url_for('customer'))
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        grandtotal += int(product['price'])*int(product['quantity'])
    
    return render_template('product/cart.html', grandtotal = grandtotal)

@app.route('/updatecart/<int:code>', methods = ['POST'])
def updateCart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <=0:
        return redirect(url_for('customer'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash(f'Item {item.name} is updated.')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <=0:
        return redirect(url_for('customer'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearCart():
    try:
        session.pop('Shoppingcart', None)
        flash(f'Cart is cleared.', 'danger')
        return redirect(url_for('customer'))
    except Exception as e:
        print(e)
        return redirect(url_for('customer'))