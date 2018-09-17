from app import db
from modules.orders.mod_orders import ModOrders
from modules.pays.mod_pays import ModPays
from modules.pays.pays import calcPayOrder, selectPaysOrder, calcPaysOrder, calcPayment, allPays, allDatePays, addpay_order
from models import Orders, OrdersType, Status, Status_pay, Pays
import sys
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/core')
sys.path.insert(0,'/app/modules/orders')

def allOrders():
    query = Orders.query.all()
    return query

def infoOrder(ord_num):
    """Information about order"""
    ord_num = Orders.query.filter(Orders.ord_num==ord_num).first()
    return ord_num

def viewOrder(order_id):
    query = Orders.query.filter_by(id=order_id).first()
    return query

def viewOrderType(id):
    query = OrdersType.query.filter_by(id=id).first()
    return query

def addOrder(**kwargs):
    """Add an order to the database"""
    db.session.close()
    item = ModOrders()
    data = item.add(**kwargs)
    if infoOrder(data['ord_num']):
        error = 'error'
        return error
    a = Orders(**data)
    db.session.add(a)
    db.session.commit()
    ord_id = Orders.query.filter_by(ord_num=data['ord_num']).first()
    return ord_id

def addOrderType(**kwargs):
    """ Add an order type to the database"""
    db.session.close()
    at = OrdersType(**kwargs)
    db.session.add(at)
    db.session.commit()
    return 'Save OrderType'

def listsum(n):
    """Подсчет суммы"""
    count = 0
    for i in n:
        count = count + i
    return count

def discountOrder(summa,discount_percent,discount_sum):
    """Расчет скидки %"""
    if discount_percent == 100 or discount_sum >= summa:
        return summa
    if summa != 0:
        if discount_percent != 0:
            discount_percent= summa/100*discount_percent
        discount = discount_percent + discount_sum
        return discount
    else:
        discount = discount_sum
    return discount

def editDiscountOrder(order_id,**update):
    """Редактировать discount """
    if update != {}:
        db.session.query(Orders).filter(Orders.id == order_id).update(update)
        db.session.commit()
    return 'Done'

def selectOrderType(order_id):
    """Выборка по order_id и подсчет суммы заказа """
    query = OrdersType.query.filter_by(oid=int(order_id)).all()
    query = [(i,i.quantity * i.quantity_sum if i.quantity >= 1 else 0 if i.quantity_sum==0 else 0) for i in query]
    type_sum = listsum([n[1] for n in query])
    return query,type_sum

def editQuantity(quantity_id,**update):
    """Редактировать наименнование по ordertype_id"""
    if update != {}:
        db.session.query(OrdersType).filter(OrdersType.id == quantity_id).update(update)
        db.session.commit()
    return 'Done'

def deleteQuantity(quantity_id):
    """ Удалить наименнование по id"""
    query = OrdersType.query.filter_by(id=quantity_id).first()
    if query != None:
        db.session.delete(query)
        db.session.commit()
        oid = query.oid
    else:
        oid = 'None'
    return oid
