from wtforms import Form, IntegerField, StringField, validators, SelectField, RadioField 
from shop import db
from shop.admin.state import state_list
import json

class AddcardForm(Form):
    card_number = StringField('Card Nunber', [validators.Length(min=16, max=16), validators.DataRequired()])
    card_owner_name = StringField('Owner Name', [validators.Length(min=2, max=40), validators.DataRequired()])
    card_expire_date = StringField('Expire Date', [validators.Length(min=4, max=4), validators.DataRequired()])
    card_cvv =  StringField('CVV (3-digit)', [validators.Length(min=3, max=3), validators.DataRequired()])
    CBA_line_one = StringField('Line 1', [validators.Length(max=100), validators.DataRequired()])
    CBA_line_two = StringField('Line 2', [validators.Length(max=100), validators.DataRequired()])
    CBA_city =  StringField('City', [validators.Length(min=2, max=50), validators.DataRequired()])
    CBA_state = SelectField('State', choices= state_list , coerce= str)
    CBA_zipcode = StringField('Zip Code (5-digit)', [validators.Length(min=5, max=5), validators.DataRequired()])

class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text
    def set_value(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def get_value(self, value, dialect):
        if value is None:
            return json.loads(value)

class Checkout(Form):
    customer_id = IntegerField('Customer ID', [validators.DataRequired()])
    customer_name = StringField('Customer Name', [validators.DataRequired()])
    payment_card_number = SelectField('Debit/Credit Card Number',coerce=int)