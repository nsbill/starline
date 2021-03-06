from app import db
from datetime import datetime
from sqlalchemy.dialects import postgresql
from flask_security import UserMixin, RoleMixin
from sqlalchemy.sql.functions import current_timestamp

roles_users = db.Table('roles_users',
        db.Column('admin_user_id', db.Integer(), db.ForeignKey('admin_user.id')),
        db.Column('admin_role_id', db.Integer(), db.ForeignKey('admin_role.id')),
    )


class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer(),primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100))
    create = db.Column(db.DateTime(), default=current_timestamp())
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean,default=False)
    descr = db.Column(db.String(255))
    roles = db.relationship('AdminRole', secondary=roles_users, backref=db.backref('adminusers', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(AdminUser, self).__init__(*args, **kwargs)
    def __repr__(self):
        return '<User %r>' % self.login

class AdminRole(db.Model, RoleMixin):
    __tablename__ = 'admin_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    descr = db.Column(db.String(255))

class Orders(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
#    oid = db.Column('oid', db.Integer(), unique=True, nullable=False)
    ord_num = db.Column('ord_num', db.String(20), unique=True, nullable=False)
    create_date = db.Column('create_date', db.DateTime(), default=current_timestamp())
    complete_date = db.Column('complete',db.DateTime())
    client = db.Column('client', db.String(120), default='unknow')
    phone = db.Column('phone', db.String(32), default='0')
    discount = db.Column('discount', db.Integer(), default=0)
    discount_sum = db.Column('discount_sum', db.Integer(), default=0)
    orders_type_id = db.relationship('OrdersType', backref='orders', lazy='dynamic')
    status_id = db.Column('status_id',db.Integer(), db.ForeignKey('status.id'))
    descr = db.Column('descr', db.Text())
    csrf_token = db.Column('token', db.String(91))

class OrdersType(db.Model):
    __tablename__='orders_type'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('name', db.String(120), nullable=False)
    quantity = db.Column('quantity', db.Float(), nullable=False)
    quantity_sum = db.Column('quantity_sum', db.Float(), nullable=False)
    oid = db.Column('oid',db.Integer(), db.ForeignKey('orders.id'))
    status_ord_id = db.Column('status_ord_id',db.Integer(), db.ForeignKey('status.id'))
    units = db.Column('units', db.String(10))
    csrf_token_ordertype = db.Column('token', db.String(91))

class Status(db.Model):
    __tablename__='status'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('name', db.String(20), nullable=False)
    status_id = db.relationship('Orders',backref='status', lazy='dynamic')
    status_ord_id = db.relationship('OrdersType',backref='status', lazy='dynamic')


class Status_pay(db.Model):
    __tablename__='status_pay'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('name', db.String(20), nullable=False)

class Pays(db.Model):
    """Оплаты"""
    __tablename__='pays'
    id = db.Column(db.Integer(), primary_key=True)
    oid = db.Column('oid',db.Integer(), db.ForeignKey('orders.id'))
#    oid_type_id = db.Column('oid_type_id',db.Integer(), db.ForeignKey('orders_type.id'))
    pay = db.Column('pay', db.Float())
    pay_date = db.Column('pay_date',db.DateTime(), default=current_timestamp())
#    prepayment = db.Column('prepayment', db.Float())
#    prepayment_date = db.Column('prepayment_date',db.DateTime())
    status_pay_id = db.Column('status_pay_id', db.Integer(), db.ForeignKey('status_pay.id'))
    units = db.Column('units', db.String(10))
    pay_descr = db.Column('pay_descr', db.Text())

class Incoming(db.Model):
    """ Приходная накладная """
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column('date', db.DateTime())
    number = db.Column('number', db.Integer(), nullable=False)
    vendor = db.Column('code',db.Integer())
    name = db.Column('vendor', db.String(255), nullable=False)
    units = db.Column('utits', db.String(10))
    quantity = db.Column('quantity', db.Float())
    value = db.Column('value', db.Float())
    amount = db.Column('amount', db.Float())
    pay_info = db.Column('pay_info',db.Integer())
    oid = db.Column('oid',db.Integer(), db.ForeignKey('orders.id'))
    gid = db.Column('gid',db.Integer(), db.ForeignKey('group_product.id'))
    sid = db.Column('sid',db.Integer(), db.ForeignKey('supplier.id'))

class Expense(db.Model):
    """Расходная накладная"""
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column('date', db.DateTime())
    number = db.Column('number', db.Integer(), nullable=False)
    vendor = db.Column('vendor',db.Integer())
    name = db.Column('name', db.String(255), nullable=False)
    units = db.Column('utits', db.String(10))
    quantity = db.Column('quantity', db.Float())
    value = db.Column('value', db.Float())
    amount = db.Column('amount', db.Float())
    pay_info = db.Column('pay_info',db.Integer())
    oid = db.Column('oid',db.Integer(), db.ForeignKey('orders.id'))
    gid = db.Column('gid',db.Integer(), db.ForeignKey('group_product.id'))
    sid = db.Column('sid',db.Integer(), db.ForeignKey('supplier.id'))

class GroupProduct(db.Model):
    """Группы наименований"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('name', db.String(50))
    descr = db.Column('descr', db.String(240))

class Supplier(db.Model):
    """Поставщики """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('name', db.String(50))
    phone = db.Column('phone', db.String(50))
    address = db.Column('address', db.String(120))
    descr = db.Column('descr', db.String(240))

#store_ven_incoming = db.Table('store_ven_id',
#        db.Column('store_id', db.Integer(), db.ForeignKey('store.id')),
#        db.Column('store_incoming_id', db.Integer(), db.ForeignKey('store_incoming.id')),
#    )
class Store(db.Model):
    """Склад"""
    __tablename__ = 'store'
    id = db.Column(db.Integer(), primary_key=True)
    vendor = db.Column('vendor',db.Integer())
    units = db.Column('units', db.String(10))
    quantity = db.Column('quantity', db.Float())
    quantity_sum = db.Column('quantity_sum', db.Float(), nullable=False)
    total_sum = db.Column('total_sum', db.Float(), nullable=False,default=0)
    gid = db.Column('gid',db.Integer(), db.ForeignKey('group_product.id'))
    store_incominges = db.relationship('StoreIncoming', backref='storeincoming',lazy='dynamic')
#    list_vendor = db.relationship('StoreIncoming', secondary=store_ven_incoming, backref=db.backref('storeincoming', lazy='dynamic'))

class StoreIncoming(db.Model):
    """Склад приход"""
    __tablename__ = 'store_incoming'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column('date',db.DateTime(), default=current_timestamp())
    vendor = db.Column('vendor',db.Integer())
    name = db.Column('name', db.String(255), nullable=False)
    units = db.Column('units', db.String(10))
    quantity = db.Column('quantity', db.Float())
    quantity_sum = db.Column('quantity_sum', db.Float(), nullable=False)
    total_sum = db.Column('total_sum', db.Float(), nullable=False,default=0)
    descr = db.Column('descr', db.String(240))
    gid = db.Column('gid',db.Integer(), db.ForeignKey('group_product.id'))
    store_id = db.Column('store_id',db.Integer(), db.ForeignKey('store.id'))

class StoreIncomingTemp(db.Model):
    __tablename__ = 'store_incoming_temp'
    id = db.Column(db.Integer(), primary_key=True)
    ord_tmp_id = db.Column('ord_tmp_id',db.Integer())
    date = db.Column('date',db.DateTime(), default=current_timestamp())
    vendor = db.Column('vendor',db.Integer())
    name = db.Column('name', db.String(255), nullable=False)
    units = db.Column('units', db.String(10))
    quantity = db.Column('quantity', db.Float())
    quantity_sum = db.Column('quantity_sum', db.Float(), nullable=False)
    total_sum = db.Column('total_sum', db.Float(), nullable=False,default=0)
    descr = db.Column('descr', db.String(240))
    gid = db.Column('gid',db.Integer(), db.ForeignKey('group_product.id'))
    store_id = db.Column('store_id',db.Integer(), db.ForeignKey('store.id'))

class ExpenseCompany(db.Model):
    """Расходы фирмы"""
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column('date',db.DateTime(), default=current_timestamp())
    name = db.Column('name', db.String(255), nullable=False)
    quantity_sum = db.Column('quantity_sum', db.Float(), nullable=False)
    descr = db.Column('descr', db.String(240))

#class Fees(db.Model):
#    pass


#
#class Users(db.Model):
#    __tablename__ = 'users'
#    id = db.Column(db.Integer, primary_key=True)
#    uid = db.Column(db.Integer, unique=True, nullable=False)
#    login = db.Column(db.String(20), unique=True, nullable=False)
#    password = db.Column(db.String(50))
#    fio = db.Column(db.String(150))
#    phone = db.Column(db.String(12), default='0')
#    descr = db.Column(db.Text)
#    disable = db.Column(db.Boolean, default=False)
#    delete = db.Column(db.Boolean, default=False)
#
#    def __init__(self,uid,login,password,fio,phone,descr,disable,delete):
#        self.uid = uid
#        self.login = login
#        self.password = password
#        self.fio = fio
#        self.phone = phone
#        self.descr = descr
#        self.disable = disable
#        self.delete = delete
#
#    def __repr__(self):
#        return "'UID': '{}', 'Login': '{}', 'Password': '{}', 'FIO': '{}', 'Phone':'{}', 'Disable':'{}'".format(self.uid, self.login, self.password, self.fio, self.phone, self.disable)
