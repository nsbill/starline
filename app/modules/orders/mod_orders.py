from datetime import datetime

class ModOrders:
    '''Ордер заказа'''
    def __init__(self, create_date=datetime.now()):
#        self.oid = '0'
        self.ord_num = ''
        self.create_date = create_date
        self.client = ''
        self.phone = ''
        self.discount = 0
        self.discount_sum = 0
        self.descr = ''
        self.csrf_token = ''

    def show(self):
        '''Просмотр ордера'''
        descr = dict(zip(['ord_num',
                        'create_date',
                        'client',
                        'phone',
                        'discount',
                        'discount_sum',
                        'descr',
                        'csrf_token'],
                                (self.ord_num,
                                self.create_date,
                                self.client,
                                self.phone,
                                self.discount,
                                self.discount_sum,
                                self.descr,
                                self.csrf_token
                                )))
        return descr

    def add(self, **kwargs):
        '''Создание ордера'''
        self.kwargs = self.show()
        for i in kwargs:
            self.kwargs[i] = kwargs[i]
        return self.kwargs

#    def addtype(self, **kwargs):
#        '''Add an order type '''
#        return self.kwargs

    def edit(self):
        '''Редактирование ордера'''
        pass

    def delete(self):
        '''Удаление ордера'''
        pass
