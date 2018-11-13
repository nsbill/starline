from datetime import datetime

class ModStore:
    """Модуль для склада"""
    def __init__(self):
        self.name=''

    def default(self):
        data = {'vendor': '',
                'name': '',
                'quantity': '',
                'quantity_sum': '',
                'descr': '',
                'csrf_token': '',
                }
        return data

    def add(self, **kwargs):
        """ Добавить позицию """
        self.kwargs = self.default()
        for i in self.kwargs:
            self.kwargs[i] = kwargs[i]
        return self.kwargs

    def additems(**kwargs):
        data = []
        for i in kwargs:
            data.append(i)
        return data

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
