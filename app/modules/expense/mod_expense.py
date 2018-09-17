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
