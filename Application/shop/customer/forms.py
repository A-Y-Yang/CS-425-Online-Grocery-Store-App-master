from wtforms import Form, IntegerField, StringField, PasswordField, validators, SelectField

class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20)])
    last_name =  StringField('Last Name', [validators.Length(min=2, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=100)])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10)])
    address_line_one = StringField('Line 1', [validators.Length(min=2, max=30)])
    address_line_two = StringField('Line 2', [validators.Length(min=2, max=30)])
    address_city = StringField('City', [validators.Length(min=2, max=20)])
    address_state = StringField('State', [validators.Length(min=2, max=20)])
    address_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5)])
    confirm = StringField('Repeat Email for Confirmation',[validators.EqualTo('email', message='Emails must match')])

class LoginForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

class Checkout(Form):
    customer_id = IntegerField('Customer ID', [validators.DataRequired()])
    customer_name = StringField('Customer Name', [validators.DataRequired()])
    payment_card_number = StringField('Debit/Credit Card Number',[validators.Length(min=16, max=16),validators.DataRequired()])