from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
#from modules.clients.modclient import Client

#from flask_admin import Admin, AdminIndexView, BaseView, expose
#from flask_admin.contrib.sqla import ModelView
#from flask_security import SQLAlchemyUserDatastore, Security, current_user

from flask import redirect, url_for, request

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


#--- ADMIN ---
#from models import AdminUser,AdminRole,Users,Address,SelectAdressUid,SortStreet,SortBuild,SortFlat,Networks,Groups,Tarifs,UsersPI,DvCalls


#class AdminMixin(BaseView):
#    def is_accessible(self):
#        return current_user.has_role('Admin')
#
#    def inaccessible_callback(self, name, **kwargs):
#        return redirect( url_for('security.login', next=request.url ))
#
#class AdminView(AdminMixin, ModelView):
#    pass
#
#class HomeAdminView(AdminMixin, AdminIndexView):
#    pass
##    @expose('/adm')
##    def index(self):
##        arg1='Home'
##        return self.render('admin/index.html',arg1=arg1)
#admin = Admin(app, 'AdminUmon', url='/', index_view=HomeAdminView(name='Home', url='/adm/'))
#admin.add_view(AdminView(AdminUser, db.session, url='/adm/adminuser'))
#admin.add_view(AdminView(AdminRole, db.session, url='/adm/adminrole'))
#admin.add_view(AdminView(Users, db.session, url='/adm/users'))
#admin.add_view(AdminView(Address, db.session, url='/adm/address'))
##admin.add_view(AdminView(SelectAdressUid, db.session, url='/adm/selectaddressuid'))
#admin.add_view(AdminView(SortStreet, db.session, url='/adm/sortstreet'))
#admin.add_view(AdminView(SortBuild, db.session, url='/adm/sortbuild'))
#admin.add_view(AdminView(SortFlat, db.session, url='/adm/sortflat'))
#admin.add_view(AdminView(Networks, db.session, url='/adm/networks'))
#admin.add_view(AdminView(Groups, db.session, url='/adm/groups'))
#admin.add_view(AdminView(Tarifs, db.session, url='/adm/tarifs'))
#admin.add_view(AdminView(UsersPI, db.session, url='/adm/userspi'))
#admin.add_view(AdminView(DvCalls, db.session, url='/adm/dvcalls'))
#
##--- Admin Flask Security ---
#
#user_datastore = SQLAlchemyUserDatastore(db, AdminUser,AdminRole)
#security = Security(app, user_datastore)
