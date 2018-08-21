from datetime import datetime

class ModPays:
    '''Оплаты'''
    def __init__(self):
        self.pay = ''
        self.pay_descr = ''

    def show(self):
        '''Просмотр оплаты'''
        data = dict(zip(['pay',
                         'pay_descr' ],
                                (self.pay,
                                 self.pay_descr
                                )))
        return data

    def add(self, **kwargs):
        '''Создание платежа'''
        self.kwargs = self.show()
        for i in kwargs:
            self.kwargs[i] = kwargs[i]
        return self.kwargs

    def edit(self):
        '''Редактирование'''
        pass

    def delete(self):
        '''Удаление'''
        pass
