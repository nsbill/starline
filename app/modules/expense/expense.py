from app import db
import sys
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
