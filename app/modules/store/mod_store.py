from datetime import datetime

class ModStore:
    ''' Модуль для склада'''
    def __init__(self):
        self.vendor = ''
        self.name = ''
        self.quantity = ''
        self.quantity_sum = ''
#        self.units = ''
        self.descr = ''
        self.csrf_token = ''

    def all(self):
        """ Выборка всех даных """
        data = dict(zip(['vendor',
                        'name',
                        'quantity',
                        'quantity_sum',
                        'descr',
                        'csrf_token'],
                                (self.vendor,
                                self.name,
                                self.quantity,
                                self.quantity_sum,
                                self.descr,
                                self.csrf_token
                                )))
        return data

    def add(self, **kwargs):
        """ Добавить позицию """
        self.kwargs = self.show()
        for i in kwargs:
            self.kwargs[i] = kwargs[i]
        return self.kwargs

    def grproduct(self, **kwargs):
	"""Группы"""
       self.add = self.add()

#    def addtype(self, **kwargs):
#        '''Add an order type '''
#        return self.kwargs

#    def edit(self):
#        '''Редактирование '''
#        pass
#
#    def delete(self):
#        '''Удаление'''
#        pass
