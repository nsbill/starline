from flask import Blueprint
from flask import render_template,request,redirect
from flask import url_for
from flask_wtf import FlaskForm
#import datetime
from datetime import datetime, date, timedelta
from time import strptime
import sys
from modules.mod_date import ModDatetime
from .forms import  OrderForm, OrderTypeForm, PayForm, DiscountForm, EditOrderForm 

sys.path.insert(0, '/app/core')
core = Blueprint('core',__name__, template_folder='templates')

from orders import allOrders, infoOrder, addOrder, addOrderType, viewOrder, viewOrderType, selectOrderType, discountOrder, editQuantity, deleteQuantity, addpay_order, calcPayOrder, selectPaysOrder, calcPaysOrder, calcPayment, editDiscountOrder, allPays, allDatePays


@core.route('/', methods=['GET'])
def index():
    ''' Стартовая страница '''
#    search = request.args.get('search')
#    if search:
#        search = searchClients(search)
#        return render_template('/user/all.html',allClients=search)
#    else:
#        return redirect('/core/users/all')
    return render_template('index.html')

@core.route('/orders/all', methods=['GET'])
def orders():
    ''' Список заказов '''
    orders = allOrders()
    return render_template('orders/all.html', allOrders=orders)

@core.route('/orders/create', methods=['POST','GET'])
def create():
    ''' Добавить ордер '''
    form_order = OrderForm()
    info = request.form.to_dict()
    print('-'*20)
    print(info)
    if form_order.validate_on_submit():
        add = []
        for i in form_order:
            if i.data != None:
                add.append((i.name,i.data))
        add_order = dict(add)
        add = addOrder(**add_order)
#        print('=add+'*20)
#        print(add.id)
        if add == 'error':
            error = 'Ошибка договор с номером '+ add_order['ord_num']+' существует'
            return render_template('orders/create.html',form_order=form_order, error=error)
        else:
            return redirect('core/orders/addtype/'+ str(add.id))
    return render_template('orders/create.html',form_order=form_order)

@core.route('/orders/addtype/<order_id>', methods=['POST','GET'])
def addtype(order_id):
    ''' Добавлять наименование '''
    view_order = viewOrder(order_id)
    discount_sum = view_order.discount_sum
    form_ordertype = OrderTypeForm()
    form_discount = DiscountForm()
#    data = [i for i in view_order]
    if request.method == 'POST':
        if form_discount.data['csrf_token_discount'] == '':
            form_discount.data['errors'] = ''
        else:
            if form_discount.validate_on_submit():
                add = []
                for i in form_discount:
                    add.append((i.name, i.data))
                update = dict(add)
                update['csrf_token'] = update.pop('csrf_token_discount')
                edit_discount = editDiscountOrder(order_id,**update)
                if edit_discount == 'Done':
                    return redirect('core/orders/addtype/'+ str(order_id))

        if form_ordertype.data['csrf_token_ordertype'] == '':
            form_ordertype.data['errors'] = ''
        else:
            if form_ordertype.validate_on_submit():
                add = []
                for i in form_ordertype:
                    if i.data != None:
                        add.append((i.name, i.data))
                add_order_type= dict(add)
                add_order_type['oid'] = int(order_id)
                add_order_type = addOrderType(**add_order_type)
                return redirect('core/orders/addtype/'+ order_id)
    sot = selectOrderType(order_id) # Выборка наименований заказа
    orders_sum = sot[1]
    discount = discountOrder(orders_sum,view_order.discount, discount_sum) # Расчет скидки

    pays = calcPayOrder(sot,discount) # Расчет суммы оплат
#    selectPays = selectPaysOrder(order_id)
    selectPays = calcPaysOrder(order_id)
    if selectPays:
        pays_sum_order = selectPays[1]
    else:
        pays_sum_order = 0
    calcOrderSum = calcPayment(orders_sum,discount,pays_sum_order)
    return render_template('orders/addtype.html',view_order=view_order, form_ordertype=form_ordertype, sot=sot,discount=discount,pays=pays, selectPays=selectPays, calcOrderSum=calcOrderSum, form_discount=form_discount)

@core.route('/orders/editorder/<order_id>', methods=['GET','POST'])
def editorder(order_id):
    """Редактирование заказчика"""
    order = viewOrder(order_id)
    form_order = EditOrderForm()
    upd = []
    if request.method == 'POST':
        if form_order.validate_on_submit():
            for i in form_order:
                upd.append((i.name, i.data))
        update = dict(upd)
        print('-'*30)
        print(update)
        upd_order = editDiscountOrder(order_id,**update)
        if upd_order == 'Done':
            return redirect('core/orders/addtype/'+str(order_id))
        else:
            return redirect('core/orders/all')
    return render_template('orders/editorder.html',form_order=form_order, order=order)

@core.route('/orders/edittype/<quantity_id>', methods=['GET','POST'])
def edittype(quantity_id):
    """Редактирование наименование"""
    form_ordertype = OrderTypeForm()
    ordertype = viewOrderType(quantity_id)
    add = []
    if request.method == 'POST':
        if form_ordertype.validate_on_submit():
            for i in form_ordertype:
                add.append((i.name, i.data))
        update = dict(add)
        edit_quantity = editQuantity(quantity_id,**update)
        if edit_quantity == 'Done':
            return redirect('core/orders/addtype/'+ str(ordertype.oid))
        else:
            return redirect('core/orders/all')
    return render_template('orders/edittype.html',form_ordertype=form_ordertype, ordertype=ordertype)


@core.route('/orders/deltype/<quantity_id>', methods=['GET','POST'])
def deltype(quantity_id):
    """Удаление наименования"""
    ordertype = viewOrderType(quantity_id)
    if request.method == 'POST':
        delete_quantity = deleteQuantity(quantity_id)
        if delete_quantity == 'None':
            return redirect('/')
        return redirect('core/orders/addtype/'+ str(delete_quantity))
    return render_template('orders/deletetype.html', ordertype=ordertype)


@core.route('/pays/allpays', methods=['GET','POST'])
def allpays():
    """Оплаты"""
    data = allPays()
    day = {}
    day['dmyw'] = date.today().strftime('01-%m-%Y')
    day['dmyf'] = date.today().strftime('%d-%m-%Y')

#    def last_day_of_month(date):
#        ''' last_day_of_month(datetime.datetime(2018,9,11)) '''
#        if date.month == 12:
#            return date.replace(day=31)
#        date = date.replace(month=date.month+1, day=1) - timedelta(days=1)
#        return date.strftime('%d-%m-%Y')
#
#    def reverse_date(d):
#        '''Разварачивает дату с ДД-ММ-ГГГГ на ГГГГ-ММ-ДД'''
#        try:
#            n = strptime(d, '%d-%m-%Y')
#            date = str(n.tm_year)+'-'+str(n.tm_mon)+'-'+str(n.tm_mday)
#            return date
#        except:
##            date = '-'.join(d.split('-')[::-1])
#            date = ''
#            return date
    if request.method == 'POST':
        moddatetime= ModDatetime()
        date_with = moddatetime.reverse_date(request.form['date_with'])
        date_from = moddatetime.reverse_date(request.form['date_from'])
        data = allDatePays(date_with,date_from)
        day['dmyw']=request.form['date_with']
        day['dmyf']=request.form['date_from']
#        day['mm'] = last_day_of_month(date.today())
        return render_template('pays/allpays.html', allpays=data, day=day)
    return render_template('pays/allpays.html', allpays=data, day=day)


@core.route('/pays/add/<order_id>', methods=['GET','POST'])
def pay_order(order_id):
    """Добавление платежа"""
    form_pay = PayForm(request.form)
    if request.method == 'POST' and form_pay.validate():
        add = []
        for i in form_pay:
            if i.data != None:
                add.append((i.name,i.data))
        pay = dict(add)
        add = addpay_order(order_id,**pay)
        return redirect('core/orders/addtype/'+str(order_id))
    return render_template('pays/addpay.html', form_pay=form_pay)

@core.route('/expense/allexpenses', methods=['GET','POST'])
def allexpenses():
    """Расходы"""
    return render_template('expenses/allexpense.html')

@core.route('/expense/addexpense', methods=['GET','POST'])
def addexpense():
    """Создание позиции расходов"""
    return render_template('expenses/addexpense.html')

@core.route('/error', methods=['GET'])
def error():
    '''Выдавать страницу ошибки 404'''
    return render_template('error.html')




#
#@core.route('user/uid=<uid>', methods=['GET'])
#def user(uid):
#    ''' Информация о пользователе'''
#    client = infoClient(uid)
#    return render_template('user/info.html', infoClient=client)
#
#@core.route('user/add', methods=['POST','GET'])
#def user_add():
#    ''' Добавить пользователя '''
#    form = ClientForm()
#    if form.validate_on_submit():
##        uid = request.form['uid']
##        login = request.form['login']
##        password = request.form['password']
##        activate = request.form['activate']
##        expire = request.form['expire']
##        status = request.form['status']
###        disable = request.form['disable']
##        contract_id = request.form['contract_id']
##        contract_date = request.form['contract_date']
##        company_id = request.form['company_id']
###        delete = request.form['delete']
##        descr = request.form['descr']
#        addClient(uid=form.uid.data,
#                login=form.login.data,
#                password=form.password.data,
#                activate = form.activate.data,
#                expire = form.expire.data,
#                status = form.status.data,
#                disable = form.disable.data,
#                contract_id = form.contract_id.data,
#                contract_date = form.contract_date.data,
#                company_id = form.company_id.data,
#                delete = form.delete.data,
#                descr=form.descr.data)
#        return redirect(url_for('core.index'))
#    return render_template('user/add.html',form=form)
#

