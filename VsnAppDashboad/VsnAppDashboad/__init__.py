#!venv/bin/python
import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose
from wtforms import PasswordField


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from VsnAppDashboad.models import User, Role, roles_users, Session


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


from VsnAppDashboad.customizemodels import MyModelView, UserView, SessionView


# Create admin
admin = flask_admin.Admin(
    app,
    'VSN Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap4',
)

# Flask views
@app.route('/')
def index():
    return render_template('index.html')

# Add model views
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(SessionView(Session, db.session, menu_icon_type='fa', menu_icon_value='fa-car', name="Session"))
# define a context processor for merging flask-admin's template context into the 
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()



        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('Vsn@RqTy6u'),
            roles=[user_role, super_user_role]
        )

        #first_names = [
        #    'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
        #    'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        #    'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        #]
        #last_names = [
        #    'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        #    'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        #    'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        #]
        #
        #for i in range(len(first_names)):
        #    tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
        #    tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
        #    user_datastore.create_user(
        #        first_name=first_names[i],
        #        last_name=last_names[i],
        #        email=tmp_email,
        #        password=encrypt_password(tmp_pass),
        #        roles=[user_role, ]
        #    )
        db.session.commit()
    return

import VsnAppDashboad.mobileapi