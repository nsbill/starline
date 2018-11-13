from app import db
import sys
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/core')
sys.path.insert(0,'/app/modules/store')

from models import Store, StoreIncoming, GroupProduct
from mod_store import ModStore
#from mod_groupstore import ModGroupStore

def allStore():
    """Выборка всех позиций с таб. Store"""
    query = Store.query.all()
    return query

def allStoreIncoming():
    """Выборка всех позиций с таб. StoreIncoming"""
    query = StoreIncoming.query.all()
    return query

def addStore(**kwargs):
    """Добавить в таб. Store"""
    db.session.close()
    add = ModStore.add(**kwargs)
    data = Store(**add)
    db.session.add(data)
    db.session.commit()
    db.session.close()
    return kwargs

def checkVendorStore(**kwargs):
    """Проверить vendor в таб. Store"""
    query = Store.query.filter_by(vendor=kwargs.get('vendor')).first()
    if query == None:
        del kwargs['name']
        del kwargs['descr']
        addStore(**kwargs)
        return 'ADD'
    else:
        data = query.__dict__
        del data['_sa_instance_state']
        return data
    return None

def compareDataStore(**kwargs):
    """Сравнить данные """
    data = checkVendorStore(**kwargs)
    if data == None:
        return None
    else:
        del kwargs['name']
        del kwargs['descr']
        if kwargs.get('vendor') == data.get('vendor') and kwargs.get('gid') == data.get('gid') and kwargs.get('units') == data.get('units'):
            print('UPDATE '+kwargs)
        else:
            addStore(**kwargs)
            return data
    return kwargs

def addStoreIncoming(**kwargs):
    """ Add an expense_company type to the database"""
    db.session.close()
    data = StoreIncoming(**kwargs)
    db.session.add(data)
    db.session.commit()
    return kwargs

def viewStoreIncomingId(id):
    """ Просмотр затрат в таб. StoreIncoming по ID"""
    query = StoreIncoming.query.filter_by(id=id).first()
    return query

def editStoreIncomingId(id,**update):
    """ Редактировать позицию в таб. StoreIncoming по ID"""
    if update != {}:
        print('=*=_edit'*10)
        print(update)
        db.session.query(StoreIncoming).filter(StoreIncoming.id == id).update(update)
        db.session.commit()
    return 'Edit an StoreIncoming'

def deleteStoreIncomingId(id):
    """ Удалить позицию в таб. StoreIncoming по ID"""
    query = StoreIncoming.query.filter_by(id=id).first()
    if query != None:
        db.session.delete(query)
        db.session.commit()
        id = query.id
    else:
        id = 'None'
    return id

# --- STORE GROUPS ---
#def allGroupProduct():
#    """ Выборка всех наименований из GroupProduct """
#    query = GroupProduct.query.all()
#    return query

def listStoreIncomingGID(gid):
    """Выборка всех наменований по GID с таб. group_product"""
    query = StoreIncoming.query.filter_by(gid=gid).all()
    return query

#def viewGroupProduct(id):
#    query = GroupProduct.query.filter_by(id=id).first()
#    return query

#def addGroupProduct(**kwargs):
#    """ Add an expense_company type to the database"""
#    db.session.close()
#    data = GroupProduct(**kwargs)
#    db.session.add(data)
#    db.session.commit()
#    return 'Add an GroupProduct'

