class ModExpense:
    """ Модуль расхода фирм """
    def __init__(self):
        self.name = ''
        self.quantity_sum = ''
        self.descr = ''

    def all(self):
        """ Выборка всех даных из таб. ExpenseCompany"""
        data = dict(zip(['id',
#            'date',
            'name',
            'quantity_sum',
            'descr'],
                (self.id,
#                 self.date,
                 self.name,
                 self.quantity_sum,
                 self.descr
                 )))
        return data

    def add(self, **kwargs):
        """ Добавить"""
        self.kwargs = self.show()
        for i in kwargs:
            self.kwargs[i] = kwargs[i]
        return self.kwargs



#from app import db
#from modules.orders.mod_orders import ModOrders
#from modules.pays.mod_pays import ModPays
#from models import Orders, OrdersType, Status, Status_pay, Pays, ExpenseCompany, Expense, Store
#import sys
##import time
#sys.path.insert(0, '/app/db')
#sys.path.insert(0, '/app/core')
#sys.path.insert(0,'/app/modules/orders')
#
#def allExpense():
#    """Выборка всех даных из таб. ExpenseCompany"""
#    query = ExpenseCompany.query.all()
#    return query
#
#def viewExpense(exp_num):
#    """Просморт позиции из таб. ExpenseCompany"""
#    exp_num = ExpenseCompany.query.filter(ExpenseCompany.exp_num==exp_num).first()
#    return exp_num
#
#def editExpense(exp_num):
#    """Внести данные в таб. ExpenseCompany"""
#    pass
#
#def writeExpense(exp_num):
#    """Внести данные в таб. ExpenseCompany"""
#    pass
#
#def deleteExpense():
#    """Удалить данные из таб. ExpenseCompany"""
#    pass
