from flask import Blueprint
from flask import render_template,request,redirect
from flask import url_for
from flask_wtf import FlaskForm
#import datetime
from datetime import datetime, date, timedelta
from time import strptime
import sys
from modules.mod_date import ModDatetime
from .forms import OrderForm, OrderTypeForm, PayForm, DiscountForm, EditOrderForm, ExpenseCompanyForm, StoreForm, GroupProductForm

sys.path.insert(0, '/app/core')
sys.path.insert(0,'/app/modules/orders')
sys.path.insert(0,'/app/modules/pays')
sys.path.insert(0,'/app/modules/expense')
sys.path.insert(0,'/app/modules/store')
core = Blueprint('core',__name__, template_folder='templates')

from orders import allOrders, infoOrder, addOrder, addOrderType, viewOrder, viewOrderType, selectOrderType, discountOrder, editQuantity, deleteQuantity, editDiscountOrder
from pays import addpay_order, calcPayOrder, selectPaysOrder, calcPaysOrder, calcPayment, allPays, allDatePays, viewPay, deletePay
from expense import allExpenseCompany, addExpenseCompany, viewExpenseCompanyId, editExpenseCompanyId, deleteExpenseCompanyId
from store import allStore, addStore, listStoreGID, viewStoreId, editStoreId, deleteStoreId, allGroupProduct, viewGroupProduct, addGroupProduct

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

# --- ORDERS ---

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
    if form_order.validate_on_submit():
        add = []
        for i in form_order:
            if i.data != None:
                add.append((i.name,i.data))
        add_order = dict(add)
        add = addOrder(**add_order)
        if add == 'error':
            error = 'Ошибка договор с номером '+ add_order['ord_num']+' существует'
            return render_template('orders/create.html',form_order=form_order, error=error)
        else:
            return redirect('core/orders/addtype/'+ str(add.id))
    return render_template('orders/create.html',form_order=form_order)

@core.route('/orders/addtype/<order_id>', methods=['POST','GET'])
def addtype(order_id):
    ''' Добавить наименование '''
    view_order = viewOrder(order_id)
    discount_sum = view_order.discount_sum
    form_ordertype = OrderTypeForm()
    form_discount = DiscountForm()
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
    form_ordertype = OrderTypeForm()
    ordertype = viewOrderType(quantity_id)
    if request.method == 'POST':
        delete_quantity = deleteQuantity(quantity_id)
        if delete_quantity == 'None':
            return redirect('/')
        return redirect('core/orders/addtype/'+ str(delete_quantity))
    return render_template('orders/deletetype.html', form_ordertype=form_ordertype, ordertype=ordertype)

# --- PAYS ---

@core.route('/pays/allpays', methods=['GET','POST'])
def allpays():
    """Оплаты"""
    data = allPays()
    day = {}
    day['dmyw'] = date.today().strftime('01-%m-%Y')
    day['dmyf'] = date.today().strftime('%d-%m-%Y')

    if request.method == 'POST':
        moddatetime= ModDatetime()
        date_with = moddatetime.reverse_date(request.form['date_with'])
        date_from = moddatetime.reverse_date(request.form['date_from'])
        data = allDatePays(date_with,date_from)
        day['dmyw']=request.form['date_with']
        day['dmyf']=request.form['date_from']
#        day['mm'] = last_day_of_month(date.today())
        dataYear = ''
        return render_template('pays/allpays.html', allpays=data, day=day, dataYear=dataYear)
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

@core.route('/pays/del/<id>', methods=['GET','POST'])
def deletepay(id):
    """ Удаление оплаты по ID """
    form_pay = PayForm(request.form)
    data = viewPay(id)
    if request.method == 'POST':
        if data is not None:
            delete = deletePay(id)
            return redirect('core/orders/addtype/'+str(data.oid))
        else:
            return redirect('core/orders/all')
    return render_template('pays/delete_pay.html', form_pay=form_pay, data=data)

# --- EXPENSE ---

@core.route('/expense/allexpenses', methods=['GET','POST'])
def allexpenses():
    """Расходы"""
    return render_template('expenses/allexpense.html')

@core.route('/expense/addexpense', methods=['GET','POST'])
def addexpense():
    """Создание позиции расходов"""
    return render_template('expenses/addexpense.html')

@core.route('/expense/company/all')
def allcompanyexpense():
    """Список всех расходов для фирмы"""
    data = allExpenseCompany()
    return render_template('expenses/company/all.html',data=data)

@core.route('/expense/company/add', methods=['GET','POST'])
def addcompanyexpense():
    """Создание позиции расходов для фирмы"""
    form = ExpenseCompanyForm(request.form)
    if request.method == 'POST' and form.validate():
        add = []
        for i in form:
            if i.data != None:
                add.append((i.name,i.data))
        add_data = dict(add)
        del add_data['csrf_token']
        add = addExpenseCompany(**add_data)
        if add == 'error':
            error = 'Ошибка'
            return render_template('expense/company/add.html',form=form, error=error)
        else:
            return redirect('core/expense/company/all')
    return render_template('expenses/company/add.html', form=form)

@core.route('/expense/company/edit/<id>', methods=['GET','POST'])
def editcompanyexpense(id):
    """ Редактирование позицию затрат офиса """
    form = ExpenseCompanyForm()
    data = viewExpenseCompanyId(id)
    if request.method == 'POST' and form.validate():
        add = []
        for i in form:
            if i.data != None:
                add.append((i.name,i.data))
        update = dict(add)
        del update['csrf_token']
        edit = editExpenseCompanyId(id,**update)
        if add == 'error':
            error = 'Ошибка'
            return render_template('expense/company/edit.html',form=form, error=error)
        else:
            return redirect('core/expense/company/all')
    return render_template('expenses/company/edit.html', form=form, data=data)

@core.route('/expense/company/del/<id>', methods=['GET','POST'])
def deletecompanyexpense(id):
    """Удаление позиции затрат офиса"""
    form = ExpenseCompanyForm()
    data = viewExpenseCompanyId(id)
    if request.method == 'POST':
        delete = deleteExpenseCompanyId(id)
        if delete == 'None':
            return redirect('core/expense/company/all')
    return render_template('expenses/company/delete.html', form=form, data=data)


# --- STORE ---

@core.route('/store/all', methods=['GET','POST'])
def allstore():
    """Список всех позиций на складе """
    data = allStore()
    allgrprod = allGroupProduct()
    if request.method == 'POST':
        id=request.form['gid']
        return redirect('core/store/list/'+id)
    return render_template('store/all.html',data=data,allgrprod=allgrprod)

@core.route('/store/list/<gid>', methods=['GET','POST'])
def liststore(gid):
    """ Просмотр группы на складе """
    data = viewStoreId(gid)
    grprod_id = viewGroupProduct(gid)
    gid_list = listStoreGID(gid)
    allgrprod = allGroupProduct()
    if request.method == 'POST':
        gid=request.form['gid']
        if gid:
            return redirect('core/store/list/'+gid)
        else:
            return redirect('core/store/all')
    return render_template('store/list.html',data=data,allgrprod=allgrprod, grprod=grprod_id, gidlist=gid_list)

@core.route('/store/add', methods=['GET','POST'])
def addstore():
    """Приход на склад """
    form = StoreForm(request.form)
    allgrprod = allGroupProduct()
    if request.method == 'POST' and form.validate():
        add = []
        for i in form:
            if i.data != None:
                add.append((i.name,i.data))
        add.append(('gid',request.form['gid']))
        add_data = dict(add)
        del add_data['csrf_token']
        add = addStore(**add_data)
        if add == 'error':
            error = 'Ошибка'
            return render_template('store/add.html',form=form, error=error)
        else:
            return redirect('core/store/all')
    return render_template('store/add.html', form=form, data = allgrprod)

@core.route('/store/edit/<id>', methods=['GET','POST'])
def editstore(id):
    """ Редактирование позицию на складе """
    form = StoreForm()
    data = viewStoreId(id)
    grprod_id = viewGroupProduct(data.gid)
    allgrprod = allGroupProduct()
    if request.method == 'POST' and form.validate():
        add = []
        for i in form:
            if i.data != None:
                add.append((i.name,i.data))
        add.append(('gid',request.form['gid']))
        update = dict(add)
        del update['csrf_token']
        edit = editStoreId(id,**update)
        if add == 'error':
            error = 'Ошибка'
            return render_template('store/edit.html',form=form, error=error)
        else:
            return redirect('core/store/all')
    return render_template('store/edit.html', form=form, data=data, allgrprod=allgrprod, grprod=grprod_id)

@core.route('/store/addexpense/<order_id>', methods=['GET','POST'])
def addexpensestore(order_id):
    """ Создание расходной накладной """
    date_today = date.today().strftime('%Y-%m-%d')
    form = StoreForm()
    allgrprod = allGroupProduct()
    allstore = allStore()
#    grprod_id = viewGroupProduct(gid)
    data = {}
    data['order_id']=order_id
    data['allgrprod']=allgrprod
    data['allstore']=allstore
#    data['grprod_id']=grprod_id
    if request.method == 'POST':
        print('-'*30)
        print(request.form)
#        form_materials = list(request.form)
        print('----cancel_material----'*8)
        materials = request.form.to_dict()
        print(materials)
#        materials = []
        cancel=[]
        for key,val in materials.items():
            print(key,val)
            if key[0:3] == '000':
                print('-del==='*20)
                cancel.append(key)
                cancel.append(str(int(key)))
#            else:
#                materials.append((int(key),float(val)))
#        print('-----'*8)
#        print(cancel)
        for i in cancel:
            del materials[i]
        print('='*30)
        print(materials)
#        materials = [ int(i[0]) for i in materials ]
#        materials = set(materials) - set(cancel)
        materials = [ (int(key),val) for key,val in materials.items() ]
        print(materials)
        data['materials'] = set(materials)

        return render_template('store/expense.html', form=form, data=data, date_today=date_today)
    return render_template('store/expense.html', form=form, data=data, date_today=date_today)

@core.route('/store/del/<id>', methods=['GET','POST'])
def deletestore(id):
    """Удаление позиции на складе """
    form = StoreForm()
    data = viewStoreId(id)
    if request.method == 'POST':
        delete = deleteStoreId(id)
        if delete == 'None':
            return redirect('core/store/all')
        else:
            return redirect('core/store/all')
    return render_template('store/delete.html', form=form, data=data)
# --- STORE GROUP ---

@core.route('/store/groups/add', methods=['GET','POST'])
def addgroupsstore():
    """Добавить группу наименований на складе"""
    form = GroupProductForm(request.form)
    if request.method == 'POST' and form.validate():
        add = []
        for i in form:
            if i.data != None:
                add.append((i.name,i.data))
        add_data = dict(add)
        del add_data['csrf_token']
        add = addGroupProduct(**add_data)
        if add == 'error':
            error = 'Ошибка'
            return render_template('store/groups/add.html',form=form, error=error)
        else:
            return redirect('core/store/all')
    return render_template('store/groups/add.html', form=form)

@core.route('/error', methods=['GET'])
def error():
    '''Выдавать страницу ошибки 404'''
    return render_template('error.html')
