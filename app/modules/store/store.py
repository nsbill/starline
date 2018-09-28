from app import db
import sys
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/core')
sys.path.insert(0,'/app/modules/store')

from models import Store, GroupProduct

def allStore():
    query = Store.query.all()
    return query

def addStore(**kwargs):
    """ Add an expense_company type to the database"""
    db.session.close()
    data = Store(**kwargs)
    db.session.add(data)
    db.session.commit()
    return 'Add an Store'

def viewStoreId(id):
    """ Просмотр затрат в таб. Store по ID"""
    query = Store.query.filter_by(id=id).first()
    return query

def editStoreId(id,**update):
    """ Редактировать позицию в таб. Store по ID"""
    if update != {}:
        db.session.query(Store).filter(Store.id == id).update(update)
        db.session.commit()
    return 'Edit an Store'

def deleteStoreId(id):
    """ Удалить позицию в таб. Store по ID"""
    query = Store.query.filter_by(id=id).first()
    if query != None:
        db.session.delete(query)
        db.session.commit()
        id = query.id
    else:
        id = 'None'
    return id

# --- STORE GROUPS ---
def allGroupProduct():
    """ Выборка всех наименований из GroupProduct """
    query = GroupProduct.query.all()
    return query

def viewGroupProduct(id):
    query = GroupProduct.query.filter_by(id=id).first()
    return query

def addGroupProduct(**kwargs):
    """ Add an expense_company type to the database"""
    db.session.close()
    data = GroupProduct(**kwargs)
    db.session.add(data)
    db.session.commit()
    return 'Add an GroupProduct'

