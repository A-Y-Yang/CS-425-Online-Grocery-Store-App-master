from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField

class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20)], [validators.DataRequired()])
    last_name =  StringField('Last Name', [validators.Length(min=2, max=20)], [validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=100)], [validators.DataRequired()])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10)], [validators.DataRequired()])
    address_line_one = StringField('Line 1', [validators.Length(min=2, max=30)], [validators.DataRequired()])
    address_line_two = StringField('Line 2', [validators.Length(min=2, max=30)], [validators.DataRequired()])
    address_city = StringField('City', [validators.Length(min=2, max=20)], [validators.DataRequired()])
    address_state = StringField('State', [validators.Length(min=2, max=20)], [validators.DataRequired()])
    address_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5)], [validators.DataRequired()])
    confirm = StringField('Repeat Email for Confirmation',[validators.EqualTo('email', message='Emails must match')])

class LoginForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
