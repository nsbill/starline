from app import db

#from modules.orders.mod_orders import ModOrders
#from modules.pays.mod_pays import ModPays
import sys
#import time
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/core')
sys.path.insert(0,'/app/modules/expense')

from models import Expense, ExpenseCompany

def allExpenseCompany():
    query = ExpenseCompany.query.all()
    return query

def addExpenseCompany(**kwargs):
    """ Add an expense_company type to the database"""
    db.session.close()
    data = ExpenseCompany(**kwargs)
    db.session.add(data)
    db.session.commit()
    return 'Add an ExpenseCompany'

def viewExpenseCompanyId(id):
    """ Просмотр затрат офиса по ID"""
    query = ExpenseCompany.query.filter_by(id=id).first()
    return query

def editExpenseCompanyId(id,**update):
    """ Редактировать позицию затрат офиса по ID"""
    if update != {}:
        db.session.query(ExpenseCompany).filter(ExpenseCompany.id == id).update(update)
        db.session.commit()
    return 'Done'

def deleteExpenseCompanyId(id):
    """ Удалить позицию затрат офиса по ID"""
    query = ExpenseCompany.query.filter_by(id=id).first()
    if query != None:
        db.session.delete(query)
        db.session.commit()
        id = query.id
    else:
        id = 'None'
    return id

#def addOrder(**kwargs):
#    """Add an order to the database"""
#    db.session.close()
#    item = ModOrders()
#    data = item.add(**kwargs)
#    if infoOrder(data['ord_num']):
##        error = 'Order not saved. Key(ord_num)=('+data['ord_num']+') already exists.'
#        error = 'error'
#        return error
#    a = Orders(**data)
#    db.session.add(a)
#    db.session.commit()
#    ord_id = Orders.query.filter_by(ord_num=data['ord_num']).first()
#    return ord_id
#
#def addOrderType(**kwargs):
#    """ Add an order type to the database"""
#    db.session.close()
#    at = OrdersType(**kwargs)
#    db.session.add(at)
#    db.session.commit()
#    return 'Save OrderType'
#
#def listsum(n):
#    """Подсчет суммы"""
#    count = 0
#    for i in n:
#        count = count + i
#    return count
#
#def discountOrder(summa,discount_percent,discount_sum):
#    """Расчет скидки %"""
#    if discount_percent == 100 or discount_sum >= summa:
#        return summa
#    if summa != 0:
#        if discount_percent != 0:
#            discount_percent= summa/100*discount_percent
#        discount = discount_percent + discount_sum
#        return discount
#    else:
#        discount = discount_sum
#    return discount
#
#
#def calcPayOrder(order,discount):
#    """ Расчет оплаты с учетом скидки """
#    if order[1] <= 0:
#        data = order[1]
#    else:
#        data = order[1] - discount
#    return data
#
#
#def selectPaysOrder(order_id):
#    """Выборка оплат по заказу"""
#    query = Pays.query.filter_by(oid=int(order_id)).all()
#    return query
#
#def calcPaysOrder(order_id):
#    """Сумма всех оплат по заказу"""
#    data = selectPaysOrder(order_id)
#    if data:
#        summa = 0
#        for pay in data:
#            summa += float(pay.pay)
#        data = [ data, summa ]
#    return data
#
#def calcPayment(orders_sum,discount,pays_sum_order):
#    """Расчет оплаты по заказу"""
#    print(orders_sum,discount,pays_sum_order)
#    if orders_sum == 0:
#        return 0
#    data = orders_sum - discount - pays_sum_order
#    if data >= 0:
#        calc = {'orders_sum': orders_sum, 'discount': discount, 'pays_sum_order': pays_sum_order, 'surrender': 0, 'remainder': data }
#    else:
#        calc = {'orders_sum': orders_sum, 'discount': discount, 'pays_sum_order': pays_sum_order, 'surrender': data, 'remainder': 0 }
#    return calc
#
#def selectOrderType(order_id):
#    """Выборка по order_id и подсчет суммы заказа """
#    query = OrdersType.query.filter_by(oid=int(order_id)).all()
#    query = [(i,i.quantity * i.quantity_sum if i.quantity >= 1 else 0 if i.quantity_sum==0 else 0) for i in query]
#    type_sum = listsum([n[1] for n in query])
#    return query,type_sum
#
#def editQuantity(quantity_id,**update):
#    """Редактировать наименнование по ordertype_id"""
#    if update != {}:
#        db.session.query(OrdersType).filter(OrdersType.id == quantity_id).update(update)
#        db.session.commit()
#    return 'Done'
#
#
#def allPays():
#    """Выборка всех оплат"""
#    query = Pays.query.all()
#    return query
#
#def allDatePays(date_with, date_from):
#    """Выборка всех оплат по дате"""
#    if date_with == '' or date_from == '':
#        query = ''
#    else:
##        query = db.session.query(Pays).filter(Pays.pay_date > date_with).filter(Pays.pay_date >= date_from).all()
#        query = db.session.query(Pays).filter(db.func.date(Pays.pay_date) >= date_with).filter(db.func.date(Pays.pay_date) <= date_from).all()
#    return query
#
#def addpay_order(order_id, **value):
#    """ Add an pay to the database"""
#    db.session.close()
#    item = ModPays()
#    data = item.add(**value)
#    if data['csrf_token']:
#        data.pop('csrf_token') # Удалить csrf_token с словаря
#        data['oid'] = order_id
#        addpay = Pays(**data)
#        db.session.add(addpay)
#        db.session.commit()
#    return 'Done'
