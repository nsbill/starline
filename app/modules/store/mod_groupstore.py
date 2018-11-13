from app import db
from models import GroupProduct

class ModGroupStore():
    """ Класс просмотра, создание, редактирование, удаление группы с склада"""
    def __init__(self, name='', descr=''):
        """Инициализация для класса GroupStore"""
        self.name = name
        self.descr = descr

    def show(self, id):
        """Просмотреть все параметры группы по ID"""
        query = GroupProduct.query.filter_by(id=id).first()
        if query.__str__() != 'None':
            data = query.__dict__
            del data['_sa_instance_state']
            return data

    def all(self):
        """Просмотр всех групп"""
        items = GroupProduct.query.all()
        return items

    def add(self,name,descr):
        """Добавить группу"""
        data = GroupProduct(name=name, descr=descr)
        db.session.add(data)
        db.session.commit()

    def edit(self, id, **kwargs):
        """Редактировать группу"""
        db.session.query(GroupProduct).filter(GroupProduct.id==id).update(kwargs)
        db.session.commit()

    def delete(self,id):
        """Удаление группы"""
        db.session.query(GroupProduct).filter(GroupProduct.id==id).delete()
        db.session.commit()

