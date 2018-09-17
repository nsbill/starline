from app import db
from modules.pays.mod_pays import ModPays
from models import Pays
import sys
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/core')

def calcPayOrder(order,discount):
    """ Расчет оплаты с учетом скидки """
    if order[1] <= 0:
        data = order[1]
    else:
        data = order[1] - discount
    return data

def selectPaysOrder(order_id):
    """Выборка оплат по заказу"""
    query = Pays.query.filter_by(oid=int(order_id)).all()
    return query

def calcPaysOrder(order_id):
    """Сумма всех оплат по заказу"""
    data = selectPaysOrder(order_id)
    if data:
        summa = 0
        for pay in data:
            summa += float(pay.pay)
        data = [ data, summa ]
    return data

def calcPayment(orders_sum,discount,pays_sum_order):
    """Расчет оплаты по заказу"""
    if orders_sum == 0:
        return 0
    data = orders_sum - discount - pays_sum_order
    if data >= 0:
        calc = {'orders_sum': orders_sum, 'discount': discount, 'pays_sum_order': pays_sum_order, 'surrender': 0, 'remainder': data }
    else:
        calc = {'orders_sum': orders_sum, 'discount': discount, 'pays_sum_order': pays_sum_order, 'surrender': data, 'remainder': 0 }
    return calc

def allPays():
    """Выборка всех оплат"""
    query = Pays.query.all()
    return query

def allDatePays(date_with, date_from):
    """Выборка всех оплат по дате"""
    if date_with == '' or date_from == '':
        query = ''
    else:
        query = db.session.query(Pays).filter(db.func.date(Pays.pay_date) >= date_with).filter(db.func.date(Pays.pay_date) <= date_from).all()
    return query

def addpay_order(order_id, **value):
    """ Add an pay to the database"""
    db.session.close()
    item = ModPays()
    data = item.add(**value)
    if data['csrf_token']:
        data.pop('csrf_token') # Удалить csrf_token с словаря
        data['oid'] = order_id
        addpay = Pays(**data)
        db.session.add(addpay)
        db.session.commit()
    return 'Done'
