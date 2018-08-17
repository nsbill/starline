from app import db
from modules.orders.mod_orders import ModOrders
from models import Orders, OrdersType, Status, Status_pay, Pays
import sys
#import time
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/core')
sys.path.insert(0,'/app/modules/orders')

def allOrders():
    query = Orders.query.all()
    return query
#
#def searchClients(search):
#    if len(search) >= 2:
#        if search:
#            query = ClientsReg.query.filter(ClientsReg.login.contains(search)).all()
#            if query == []:
#                query = {'search': 'Нет данных по Вашему запросу'}
#        else:
#            query = ClientsReg.query.all()
#        return query
#    return {'search':'Слишком мало символов для поиска'}
#
def infoOrder(ord_num):
    """Information about order"""
    ord_num = Orders.query.filter(Orders.ord_num==ord_num).first()
    return ord_num

def addOrder(**kwargs):
    """Add an order to the database"""
    db.session.close()
    item = ModOrders()
    data = item.add(**kwargs)
    if infoOrder(data['ord_num']):
#        error = 'Order not saved. Key(ord_num)=('+data['ord_num']+') already exists.'
        error = 'error'
        return error
    a = Orders(**data)
    db.session.add(a)
    db.session.commit()
    ord_id = Orders.query.filter_by(ord_num=data['ord_num']).first()
    return ord_id

def viewOrder(order_id):
    query = Orders.query.filter_by(id=order_id).first()
    return query

def viewOrderType(id):
    query = OrdersType.query.filter_by(id=id).first()
    return query

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
    if summa != 0:
        if discount_percent != 0:
            discount_percent= summa/100*discount_percent
            print('-discount-='*3)
            print(discount_percent)
        discount = discount_percent + discount_sum
        print(discount)
        return discount
    else:
        discount = discount_sum
    return discount

def payOrder(order,discount):
    """ Расчет оплаты с учетом скидки """
    data = order[1] - discount
    return data

#count = 0 if count == N else N + 1
def selectOrderType(order_id):
    query = OrdersType.query.filter_by(oid=int(order_id)).all()
#    query = [(i,i.quantity * i.quantity_sum if i.quantity >= 1 else 0) for i in query]
    query = [(i,i.quantity * i.quantity_sum if i.quantity >= 1 else 0 if i.quantity_sum==0 else 0) for i in query]
    print('-sel_data='*20)
    print(query)
    for i in query:
        if i[1] == 0:
            print('=quantity_sum='*10)
            print(i[0].quantity_sum)
    type_sum = listsum([n[1] for n in query])
    return query,type_sum

def editQuantity(quantity_id,**update):
    query = OrdersType.query.filter_by(id=quantity_id).first()
    if update != {}:
        db.session.query(OrdersType).filter(OrdersType.id == quantity_id).update(update)
        db.session.commit()
    return query

def deleteQuantity(quantity_id):
    query = OrdersType.query.filter_by(id=quantity_id).first()
    if query != None:
        print('-query=-'*20)
        print(query)
        print(query.id)
        print(query.oid)
        db.session.delete(query)
        db.session.commit()
        oid = query.oid
    else:
        oid = 'None'
    return oid
