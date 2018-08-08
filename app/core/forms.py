from flask_wtf import FlaskForm
from wtforms import Form,IntegerField, StringField, TextAreaField, BooleanField, PasswordField, FloatField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField, DateTimeField

class OrderForm(FlaskForm):
    ord_num = StringField('ord_num', validators=[InputRequired()])
#    create_date = DateTimeField('create_date', validators=[InputRequired()])
#    complete_date = DateTimeField('complete_date', validators=[InputRequired()], format='%Y-%m-%d mm:ss')
    client = StringField('client', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    discount = IntegerField('discount',default=0)
    discount_sum = IntegerField('discount_sum',default=0)
#    orders_type_id = IntegerField('orders_type_id')
#    status_id = IntegerField('status_id')
    descr = TextAreaField('descr')
#    status_ord_id = IntegerField('status_ord_id')
#    pay = FloatField('pay', validators=[InputRequired()])
#    pay_date = DateTimeField('pay_date', validators=[InputRequired()])
#    prepayment = FloatField('prepayment', validators=[InputRequired()])
#    prepayment_date = DateTimeField('prepayment_date', validators=[InputRequired()])
#    descr_pay = TextAreaField('descr_pay', validators=[InputRequired()])

class OrderTypeForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    quantity = FloatField('quantity', validators=[InputRequired()])
    quantity_sum = FloatField('quantity_sum', validators=[InputRequired()])


#class ClientForm(FlaskForm):
#    uid = IntegerField('uid')
#    login = StringField('login', validators=[InputRequired('A login is required'), Length(min=3, max=12, message='от 3 до 12 символов')])
#    password = PasswordField('password', validators=[InputRequired()])
#    activate = DateTimeField('activate', validators=[InputRequired()])
#    expire = DateTimeField('expire')
#    status = IntegerField('status')
#    disable = BooleanField('disable')
#    contract_id = StringField('contract_id')
#    contract_date = DateTimeField('contract_date')
#    company_id = IntegerField('company')
#    delete = BooleanField('delete')
#    descr = TextAreaField('descr')

