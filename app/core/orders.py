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
    ord_id = Orders.query.filter(Orders.ord_num==data['ord_num']).first()
    return ord_id

def addOrderType(**kwargs):
    """ Add an order type to the database"""
    db.session.close()
    at = OrdersType(**kwargs)
    db.session.add(at)
    db.session.commit()
    return 'Save OrderType'

