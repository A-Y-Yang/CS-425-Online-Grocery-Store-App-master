from wtforms import Form, BooleanField, StringField, validators, SelectField, IntegerField
import email_validator

class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    last_name =  StringField('Last Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    da_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    da_line_two = StringField('Line 2', [validators.Length(max=100), validators.DataRequired()])
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
    a_line_two = StringField('Line 2', [validators.Length(max=100), validators.DataRequired()])
    a_city = StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    a_state = StringField('State', [validators.Length(min=2, max=25), validators.DataRequired()])
    a_zipcode = StringField('Zip Code', [validators.Length(min=5, max=5), validators.DataRequired()])
    salary = IntegerField('Salary', [validators.DataRequired()])
    job_title = StringField('Job Title', [validators.Length(min=1, max=20), validators.DataRequired()])
    confirm = StringField('Repeat Email for Confirmation',[validators.EqualTo('email', message='Emails must match')])

class LoginForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=20), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])
