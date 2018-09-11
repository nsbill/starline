from datetime import datetime, date, time, timedelta

class ModDatetime:
    '''Модуль для работы с датой и временем '''
    def __init__(self):
        self.datetime = datetime.now()

    def last_day_of_month(self,date):
        ''' last_day_of_month(datetime.datetime(2018,9,11)) '''
        if date.month == 12:
            return date.replace(day=31)
        date = date.replace(month=date.month+1, day=1) - timedelta(days=1)
        return date.strftime('%d-%m-%Y')

    def reverse_date(self,d):
        '''Разварачивает дату с ДД-ММ-ГГГГ на ГГГГ-ММ-ДД'''
        try:
            n = datetime.strptime(d, '%d-%m-%Y')
            date = str(n.year)+'-'+str(n.month)+'-'+str(n.day)
            return date
        except:
#            date = '-'.join(d.split('-')[::-1])
            date = ''
            return date
