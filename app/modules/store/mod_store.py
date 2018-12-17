from app import db
from models import Store, StoreIncoming, StoreIncomingTemp
from datetime import datetime

class ModStore:
    """Модуль для склада"""
    def __init__(self):
        self.name=''

    def default(self):
        data = {'vendor': '',
                'name': '',
                'units': '',
                'quantity': '',
                'quantity_sum': '',
                'total_sum': '',
                'descr': '',
                'gid': '',
                'store_id': '',
                }
        return data

    def allStore(self):
        """Выборка всех позиций с таб. Store"""
        query = Store.query.all()
        return query

    def allStoreIncoming(self):
        """Выборка всех позиций с таб. StoreIncoming"""
        query = StoreIncoming.query.all()
        return query

#    def add(self, **kwargs):
#        """ Добавить позицию """
#        self.kwargs = self.default()
#        for i in self.kwargs:
#            self.kwargs[i] = kwargs[i]
#        return self.kwargs

    def additems(**kwargs):
        data = []
        for i in kwargs:
            if 'Incoming' in i:
                data.append(i.strip('Incoming'))
#               print(dict(data))
        return data

    def addStoreIncoming(self,vendor,name,units,quantity,quantity_sum,total_sum,descr,gid,store_id):
        """Добавить StoreIncoming"""
        data = StoreIncoming(vendor=vendor,
                name=name,
                units=units,
                quantity=quantity,
                quantity_sum=quantity_sum,
                total_sum=total_sum,
                descr=descr,
                gid=gid,
                store_id=store_id,)
        print(data)
        db.session.add(data)
        db.session.commit()

    def addStoreIncomingTemp(self,ord_tmp_id,vendor,name,units,quantity,quantity_sum,total_sum,descr,gid,store_id):
        """Добавить StoreIncomingTemp"""
        data = StoreIncoming(ord_tmp_id,
                vendor=vendor,
                name=name,
                units=units,
                quantity=quantity,
                quantity_sum=quantity_sum,
                total_sum=total_sum,
                descr=descr,
                gid=gid,
                store_id=store_id,)
        print(data)
        db.session.add(data)
        db.session.commit()

    def checkVendorStore(self,vendor):
        """Проверить vendor в таб. Store"""
        query = Store.query.filter_by(vendor=vendor).first()
        if query.__str__() != 'None':
            data = query.__dict__
            del data['_sa_instance_state']
            return data

    def checkVendorStoreIncoming(self, vendor):
        """Проверить vendor в таб. StoreIncoming"""
        query = StoreIncoming.query.filter_by(vendor=vendor).first()
        if query.__str__() != 'None':
            data = query.__dict__
            del data['_sa_instance_state']
            return data

    def viewStoreIncomingId(self,id):
        """ Просмотр затрат в таб. StoreIncoming по ID"""
        query = StoreIncoming.query.filter_by(id=id).first()
        return query


    def editStoreIncomingId(self, id,**update):
        """ Редактировать позицию в таб. StoreIncoming по ID"""
        if update != {}:
            print('=*=_edit'*10)
            print(update)
            db.session.query(StoreIncoming).filter(StoreIncoming.id == id).update(update)
            db.session.commit()
        return 'Edit an StoreIncoming'

    def deleteStoreIncomingId(self, id):
        """ Удалить позицию в таб. StoreIncoming по ID"""
        query = StoreIncoming.query.filter_by(id=id).first()
        if query != None:
            db.session.delete(query)
            db.session.commit()
            id = query.id
        else:
            id = 'None'
        return id

    def listStoreIncomingGID(self, gid):
        """Выборка всех наменований по GID с таб. group_product"""
        query = StoreIncoming.query.filter_by(gid=gid).all()
        return query

    def compareDataStore(self, **kwargs):
        """Сравнить данные """
        data = checkVendorStore(kwargs)
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

#    def add(self, **kwargs):
#        """ Добавить позицию """
#        self.kwargs = self.default()
#        for i in self.kwargs:
#            self.kwargs[i] = kwargs[i]
#        return self.kwargs

##    def addtype(self, **kwargs):
##        '''Add an order type '''
##        return self.kwargs
#
#    def edit(self,*args):
#        '''Редактирование '''
#        
##
##    def delete(self):
##        '''Удаление'''
##        pass
