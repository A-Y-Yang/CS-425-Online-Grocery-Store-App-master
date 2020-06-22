from wtforms import Form, StringField, validators, SelectField, IntegerField, DecimalField, SelectMultipleField
import email_validator

class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    last_name =  StringField('Last Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    da_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    da_line_two = StringField('Line 2', [validators.Length(max=100)])
    da_city = StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    da_state = StringField('State', [validators.Length(min=2, max=25), validators.DataRequired()])
    da_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5), validators.DataRequired()])
    confirm = StringField('Repeat Email for Confirmation',[validators.EqualTo('email', message='Emails must match')])

class StaffRegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    last_name =  StringField('Last Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    a_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    a_line_two = StringField('Line 2', [validators.Length(max=100)])
    a_city = StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    a_state = StringField('State', [validators.Length(min=2, max=25), validators.DataRequired()])
    a_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5), validators.DataRequired()])
    salary = IntegerField('Salary', [validators.DataRequired()])
    job_title = StringField('Job Title', [validators.Length(min=1, max=20), validators.DataRequired()])
    confirm = StringField('Repeat Email for Confirmation',[validators.EqualTo('email', message='Emails must match')])

class LoginForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])

class Addsupplier(Form):
    name = StringField('Supplier Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    a_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    a_line_two = StringField('Line 2', [validators.Length(max=100)])
    a_city = StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    a_state = StringField('State', [validators.Length(min=2, max=25), validators.DataRequired()])
    a_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5), validators.DataRequired()])

class Addwarehouse(Form):
    name = StringField('Warehouse Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    a_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    a_line_two = StringField('Line 2', [validators.Length(max=100), validators.DataRequired()])
    a_city = StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    a_state = StringField('State', [validators.Length(min=2, max=25), validators.DataRequired()])
    a_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5), validators.DataRequired()])
    capacity =  DecimalField('Capacity (in cubic feet)', [validators.Length(max=12), validators.DataRequired()], places = 5)

class Addstock(Form):

    staff_id = StringField('Staff ID', [validators.Length(min=2, max=20), validators.DataRequired()])
    product_id = StringField('Product ID', [validators.Length(min=2, max=20), validators.DataRequired()])
    warehouse_id = StringField('Warehouse ID', [validators.Length(min=2, max=20), validators.DataRequired()])
    add_quantity = DecimalField('Quantity', [validators.Length(max=12), validators.DataRequired()], places = 2)
    add_size = DecimalField('Size (in cubic feet)', [validators.Length(max=12), validators.DataRequired()], places = 2)

class Addsupplier_product(Form):
    name = StringField('Supplier Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    a_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    a_line_two = StringField('Line 2', [validators.Length(max=100)])
    a_city = StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    a_state = StringField('State', [validators.Length(min=2, max=25), validators.DataRequired()])
    a_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5), validators.DataRequired()])
    product_supplies = SelectField('Product in Supply', coerce=int)
    product_supplier_price = DecimalField('Supplier Price', places = 2)

class Addwarehouse_product(Form):
    name = StringField('Warehouse Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    a_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    a_line_two = StringField('Line 2', [validators.Length(max=100), validators.DataRequired()])
    a_city = StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    a_state = StringField('State', [validators.Length(min=2, max=25), validators.DataRequired()])
    a_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5), validators.DataRequired()])
    capacity =  DecimalField('Capacity (in cubic feet)', [validators.Length(max=12), validators.DataRequired()], places = 5)
    product_in_stock = SelectMultipleField('Product in Stock')
    product_in_stock_quantity = IntegerField('Quantity')