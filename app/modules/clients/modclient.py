from datetime import datetime

#class Client:
#    '''Управление учетной записи клиента'''
#    def __init__(self, registration=datetime.now()):
#        self.uid = '0'
#        self.login = '0'
#        self.password = 'password'
#        self.registration = registration
#        self.activate = '2000-01-01'
#        self.expire = '2001-01-01'
#        self.status = 0
#        self.disable = 0
#        self.contract_id = ''
#        self.contract_date = '2001-01-01'
#        self.company_id = 0
#        self.delete = 0
#        self.archive = 0
#        self.bill = 0
#        self.descr = ''
#
#    def show(self):
#        '''Посмотр введенных данных'''
#        descr = dict(zip(['uid',
#                          'login',
#                          'password',
#                          'registration',
#                          'activate',
#                          'expire',
#                          'status',
#                          'disable',
#                          'contract_id',
#                          'contract_date',
#                          'company_id',
#                          'delete',
#                          'descr'],
#                                  (self.uid,
#                                   self.login,
#                                   self.password,
#                                   self.registration,
#                                   self.activate,
#                                   self.expire,
#                                   self.status,
#                                   self.disable,
#                                   self.contract_id,
#                                   self.contract_date,
#                                   self.company_id,
#                                   self.delete,
#                                   self.archive,
#                                   self.bill,
#                                   self.descr
#                                  )))
#        return descr
#
#    def add(self,**kwargs):
#        '''Создание новой учетной записи'''
#        self.kwargs = self.show()
#        for i in kwargs:
#            self.kwargs[i] = kwargs[i]
#        return self.kwargs
#
#    def edit(self):
#        '''Редактирование учетной записи'''
#        pass
#
#    def deleting(self):
#        '''Удаление учетной записи'''
#        pass
#
#    def title_fio(self):
#        '''Первую букву каждого слова переводит в верхний регистр, а все остальные в нижний'''
#        return self.fio.title()
