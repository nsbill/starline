from flask import Blueprint
from flask import render_template,request,redirect
from flask import url_for
from flask_wtf import FlaskForm
from datetime import datetime
import sys

from .forms import  OrderForm, OrderTypeForm

sys.path.insert(0, '/app/core')
core = Blueprint('core',__name__, template_folder='templates')

from orders import allOrders, infoOrder, addOrder, addOrderType


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
    ''' Добавить пользователя '''
    form_order = OrderForm()
    form_ordertype = OrderTypeForm()
#    info = request.form.to_dict()
#    print('-'*20)
#    print(info)
#    for i,k in request.form.items():
#        print(i,k)

    if form_order.validate_on_submit():
        add = []
        add_type = []
        if form_ordertype.validate_on_submit():
            for i in form_order:
                if i.data != None:
                    add.append((i.name,i.data))
            for i in form_ordertype:
                if i.data != None:
                    add_type.append((i.name, i.data))

        add_order = dict(add)
        add = addOrder(**add_order)

        if add == 'error':
            error = 'Ошибка договор с номером '+ add_order['ord_num']+' существует'
            return render_template('orders/create.html',form_order=form_order,form_ordertype=form_ordertype, error=error)
        else:
            add_order_type= dict(add_type)
            add_order_type['oid'] = int(add.id)
            add_order_type = addOrderType(**add_order_type)
            return redirect('core/orders/all')
    return render_template('orders/create.html',form_order=form_order,form_ordertype=form_ordertype)


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

