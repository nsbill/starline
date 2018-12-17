from flask import Blueprint
from flask import render_template, request, redirect,session, url_for
from flask_wtf import FlaskForm
#import datetime
from datetime import datetime, date, timedelta
from time import strptime
import sys
from modules.mod_date import ModDatetime
from .forms import OrderForm, OrderTypeForm, PayForm, DiscountForm, EditOrderForm, ExpenseCompanyForm, StoreIncomingForm, GroupProductForm

sys.path.insert(0, '/app/core')
sys.path.insert(0,'/app/modules/orders')
sys.path.insert(0,'/app/modules/pays')
sys.path.insert(0,'/app/modules/expense')
sys.path.insert(0,'/app/modules/store')
core = Blueprint('core',__name__, template_folder='templates')

from mod_store import ModStore
from mod_groupstore import ModGroupStore
from orders import allOrders, infoOrder, addOrder, addOrderType, viewOrder, viewOrderType, selectOrderType, discountOrder, editQuantity, deleteQuantity, editDiscountOrder
from pays import addpay_order, calcPayOrder, selectPaysOrder, calcPaysOrder, calcPayment, allPays, allDatePays, viewPay, deletePay
from expense import allExpense, addExpense, allExpenseCompany, addExpenseCompany, viewExpenseCompanyId, editExpenseCompanyId, deleteExpenseCompanyId
#from store import allStore, allStoreIncoming, addStoreIncoming, listStoreIncomingGID, viewStoreIncomingId, editStoreIncomingId, deleteStoreIncomingId, checkVendorStore

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
    allexpense = allExpense()
    return render_template('expenses/allexpense.html', data = allexpense)

@core.route('/expense/addexpense', methods=['POST'])
def addexpense():
    """Добавить позицию расходов"""
    if  request.method == 'POST':
        form = request.form.to_dict()
        print('---form-expense---'*9)
        print(form)
        add = addExpense(order_id,**form)
        return render_template('expenses/allexpense.html')
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
    modstore = ModStore()
    data = modstore.all()
#    data = allStore()
#    allgrprod = allGroupProduct()
    mod = ModGroupStore()
    allgrprod = mod.all()
    if request.method == 'POST':
        id=request.form['gid']
        return redirect('core/store/list/'+id)
    return render_template('store/all.html',data=data,allgrprod=allgrprod)

@core.route('/store/list/<gid>', methods=['GET','POST'])
def liststore(gid):
    """ Просмотр группы на складе """
    modstore = ModStore()
    mod = ModGroupStore()
    allgrprod = mod.all()
    grprod_id = mod.show(gid)
    data = modstore.viewStoreIncomingId(gid)
    gid_list = modstore.listStoreIncomingGID(gid)
#    allgrprod = allGroupProduct()
    if request.method == 'POST':
        gid=request.form['gid']
        if gid:
            return redirect('core/store/list/'+gid)
        else:
            return redirect('core/store/all')
    return render_template('store/list.html',data=data,allgrprod=allgrprod, grprod=grprod_id, gidlist=gid_list)

@core.route('/store/incoming/list', methods=['GET','POST'])
def incoming_list():
    """Просмотр всех наименований на склад"""
    data = modstore.allStoreIncoming()
#    allgrprod = allGroupProduct()
    mod = ModGroupStore()
    allgrprod = mod.all()
    day = {}
    day['dmyw'] = date.today().strftime('01-%m-%Y')
    day['dmyf'] = date.today().strftime('%d-%m-%Y')

    if request.method == 'POST':
        id=request.form['gid']
        return redirect('core/store/list/'+id)
    return render_template('store/incoming/list.html',data=data,allgrprod=allgrprod,day=day)

@core.route('/store/incoming/add', methods=['GET','POST'])
def addstore():
    """Приход на склад """
    date_today = date.today().strftime('%Y-%m-%d')
    form = StoreIncomingForm(request.form)
    mod = ModGroupStore()
    modstore = ModStore()
    allgrprod = mod.all()
    data={}
    data['allgrprod']=allgrprod
    gid = request.args.get('g')
    listGroupID = modstore.listStoreIncomingGID(gid)
    print('-FORM-'*10)
    print(request.args)
    print(request.form)
    addIncomItemId = list(request.form.to_dict())
    print(addIncomItemId)
    data['listGroupID'] = listGroupID
    data['incomings'] = addIncomItemId
    if request.method == 'POST':
        materials = request.form.to_dict()
        print('-=-materials==='*8)
        print(materials)
        ListAddItemsId=ModStore.additems(**materials)
#        data['ListAddItemsId'] = ListAddItemsId
        data['ListAddItemsId'] = [ modstore.viewStoreIncomingId(int(i)) for i in ListAddItemsId]
        return render_template('store/incoming/add.html', form=form, data=data, date_today=date_today)
    return render_template('store/incoming/add.html', form=form, data=data, date_today=date_today)
#        cancel=[]
#        send_expense = []
#        for key,val in materials.items():
#            if key[0:3] == '000':
#                cancel.append(key)
#                cancel.append(str(int(key)))
#            else:
#                if key[0:3] == '001':
#                    send_expense.append(key)
#        for i in cancel:
##            print('---i==='*8)
##            print(i)
#            if i:
#                del materials[i]
#        materials = [ (key,val) for key,val in materials.items() ]
#        data['materials'] = set(materials)
#        if send_expense:
#            if send_expense[0] == '001':
##                print('send_expense---'*3)
##                print(data['materials'])
##                print(send_expense)
#                data=data['materials']
##                add = addExpense()
#                return redirect('core/orders/addtype/'+str(order_id))
#    if request.method == 'POST' and form.validate():
#        add = []
#        for i in form:
#            print('-addStoreIncoming-'*10)
#            print(i)
#            if i.data != None:
#                add.append((i.name,i.data))
#        add.append(('gid',request.form['gid']))
#        add_data = dict(add)
#        add_data['total_sum'] = float(add_data['quantity']) * float(add_data['quantity_sum'])
#        del add_data['csrf_token']
#        add = addStoreIncoming(**add_data)
#        print('==ADD=addStoreIncoming=='*3)
#        print(add)
#        add_store = checkVendorStore(**add)
#        print('-add-store----'*8)
#        print(add_store)
#        if add == 'error':
#            error = 'Ошибка'
#            return render_template('store/imcoming/add.html',form=form, data=data, error=error)
#        else:
#            return redirect('core/store/all')

@core.route('/store/incoming/add/<gid>', methods=['GET','POST'])
def addlistitems(gid):
    """Выборка с группы наименования """
    modstore = ModStore()
    date_today = date.today().strftime('%Y-%m-%d')
    form = StoreIncomingForm(request.form)
    data = modstore.listStoreIncomingGID(gid)
    mod = ModGroupStore()
    allgrprod = mod.all()
    listGroupID = modstore.listStoreIncomingGID(gid)
    addIncomItemId = list(request.form.to_dict())
    data={}
    data['gid'] = gid
    data['allgrprod'] = allgrprod
    data['listGroupID'] = listGroupID
    data['incomings'] = addIncomItemId
    data['ListAddItemsId'] = []
    materials = request.form.to_dict()
    if request.method == 'POST':
        del_item_id = [ k for k, v in materials.items() if v == 'del']
        if del_item_id:
            item_id = str(del_item_id[0][8:])
            del materials[del_item_id[0]]
            del materials['Incoming' + str(item_id)]
#        save_items = request.form.get('save_items')
        save_item = [ k for k, v in materials.items() if v == 'Записать']
        print(save_item)
        if save_item:
            save_item_id = str(save_item[0][13:])
            save = [ (k,v) for k, v in materials.items() if k[:4] == 'Inc'+save_item_id]
            print(save)
        ListAddItemsId=ModStore.additems(**materials)
        print('------ListAddItemsId-----'*5)
        print(ListAddItemsId)
        print(request.form.to_dict())
        print('-FORM-'*10)
        print(request.form)
        data['ListAddItemsId'] = [ modstore.viewStoreIncomingId(int(i)) for i in ListAddItemsId]
        return render_template('store/incoming/add.html', form=form, data=data, date_today=date_today)
    return render_template('store/incoming/add.html', form=form, data=data, date_today=date_today)

@core.route('/store/incoming/edit/<id>', methods=['GET','POST'])
def editstore(id):
    """ Редактирование позицию на складе """
    modstore = ModStore()
    mod = ModGroupStore()
    form = StoreIncomingForm()
    data = modstore.viewStoreIncomingId(id)
#    grprod_id = viewGroupProduct(data.gid)
    grprod_id = mod.show(data.gid)
#    allgrprod = allGroupProduct()
    allgrprod = mod.all()
    if request.method == 'POST' and form.validate():
        add = []
        for i in form:
            if i.data != None:
                add.append((i.name,i.data))
        add.append(('gid',request.form['gid']))
        update = dict(add)
        print('==UPDATE=StoreIncoming=='*3)
        print(update)
        update['total_sum'] = float(update['quantity']) * float(update['quantity_sum'])
        del update['csrf_token']
        edit = modstor.editStoreIncomingId(id,**update)
        if add == 'error':
            error = 'Ошибка'
            return render_template('store/incoming/edit.html',form=form, error=error)
        else:
            return redirect('core/store/all')
    return render_template('store/incoming/edit.html', form=form, data=data, allgrprod=allgrprod, grprod=grprod_id)

@core.route('/store/addexpense/<order_id>', methods=['GET','POST'])
def addexpensestore(order_id):
    """ Создание расходной накладной """
    date_today = date.today().strftime('%Y-%m-%d')
    form = StoreIncomingForm()
    modstore = ModStore()
    mod = ModGroupStore()
    allgrprod = mod.all()
    allstore = modstore.allStoreIncoming()
    data = {}
    data['order_id']=order_id
    data['allgrprod']=allgrprod
    data['allstore']=allstore
    if request.method == 'POST':
        materials = request.form.to_dict()
        cancel=[]
        send_expense = []
        for key,val in materials.items():
            if key[0:3] == '000':
                cancel.append(key)
                cancel.append(str(int(key)))
            else:
                if key[0:3] == '001':
                    send_expense.append(key)
        for i in cancel:
            print('---i==='*8)
            print(i)
            if i:
                del materials[i]
        materials = [ (int(key),val) for key,val in materials.items() ]
        data['materials'] = set(materials)
        if send_expense:
            if send_expense[0] == '001':
                print('send_expense---'*3)
                print(data['materials'])
                print(send_expense)
                data=data['materials']
#                add = addExpense()
                return redirect('core/orders/addtype/'+str(order_id))
        return render_template('store/expense.html', form=form, data=data, date_today=date_today)
    return render_template('store/expense.html', form=form, data=data, date_today=date_today)

@core.route('/store/incoming/del/<id>', methods=['GET','POST'])
def deletestore(id):
    """Удаление позиции на складе """
    modstore = ModStore()
    form = StoreIncomingForm()
    data = viewStoreIncomingId(id)
    if request.method == 'POST':
        delete = modstore.deleteStoreIncomingId(id)
        if delete == 'None':
            return redirect('core/store/all')
        else:
            return redirect('core/store/all')
    return render_template('store/incoming/delete.html', form=form, data=data)

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
        mod = ModGroupStore()
        mod.add(name=add_data.get('name'),descr=add_data.get('descr'))
        return redirect('core/store/all')
    return render_template('store/groups/add.html', form=form)

@core.route('/error', methods=['GET'])
def error():
    '''Выдавать страницу ошибки 404'''
    return render_template('error.html')
