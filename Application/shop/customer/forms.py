from wtforms import Form, IntegerField, StringField, PasswordField, validators, SelectField

class Checkout(Form):
    customer_id = IntegerField('Customer ID', [validators.DataRequired()])
    customer_name = StringField('Customer Name', [validators.DataRequired()])
    payment_card_number = StringField('Debit/Credit Card Number',[validators.Length(min=16, max=16),validators.DataRequired()])