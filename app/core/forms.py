from flask_wtf import FlaskForm
from wtforms import Form,IntegerField, StringField, TextAreaField, BooleanField, PasswordField, FloatField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.fields.html5 import DateField, DateTimeField

class OrderForm(FlaskForm):
    ord_num = StringField('ord_num', validators=[InputRequired()])
#    create_date = DateTimeField('create_date', validators=[InputRequired()])
#    complete_date = DateTimeField('complete_date', validators=[InputRequired()], format='%Y-%m-%d mm:ss')
    client = StringField('client', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    discount = IntegerField('discount',default=0,validators=[InputRequired(), NumberRange(min=0,max=100, message=' Ошибка: скидка от 0 до 100%')])
    discount_sum = IntegerField('discount_sum',default=0,validators=[InputRequired(), NumberRange(min=0, message=' Ошибка: скидка от 0 руб.')])
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
#    units = StringField('units', validators=[InputRequired()])
    units = SelectField(u'units', choices=[('шт.', 'шт.'),('ед.','ед.'), ('м', 'м'), ('м2', 'м2.'),('мл.','мл.'),('услуга','услуга'),])
    quantity = FloatField('quantity', validators=[InputRequired(), NumberRange(min=1,max=100000000, message=' Ошибка ввода: кол-во от 1 ед./шт.')])
    quantity_sum = FloatField('quantity_sum', validators=[InputRequired(), NumberRange(min=0,max=100000000, message='Ошибка ввода: сумма от 0 руб')])


class PayForm(FlaskForm):
    units = SelectField(u'units', choices=[('Наличный','Наличный'),('Безнал.','Безналичный'),])
    pay = FloatField('pay')
    pay_descr = TextAreaField('pay_descr')

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

