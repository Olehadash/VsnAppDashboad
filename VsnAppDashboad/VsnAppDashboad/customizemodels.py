import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
import imghdr
from flask_admin.contrib import sqla
from flask_admin.form.upload import FileUploadField, ImageUploadField
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose, Admin
from wtforms import PasswordField, ValidationError
from jinja2 import Markup
from VsnAppDashboad.models import Imageslink
import wtforms as wtf


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True

class UserView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    #form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    form_overrides = {
        'password': PasswordField
    }

class SessionView(MyModelView):

    def _image_formatter(view, context, model, name):
        value = u"<div style = 'overflow: auto;  height:200px;'>"
        for img in model.images:
            value += u"<a href='%s'>%s</a><br>" % (img.link, img.link)
        value += "</div>"
        return Markup(
            value
        ) if model.images else ""

    def _width_count (view, context, model, name):
        return Markup(
            "<dev style = 'width: 20%'></dev>"
        )

    column_hide_backrefs = False
    #inline_models = (Imageslink,)
    column_list = ('license_number','car_type', 'apriser_name', 'playce_of_check', 'date_of_entertainment', 'date_of_check', 'name_insurance', 'agent_name','agent_phone', 'garage_name', 'garage_phone', 'googleFolder','images')
    form_columns = ['license_number','car_type', 'apriser_name', 'playce_of_check', 'date_of_entertainment', 'date_of_check', 'name_insurance', 'agent_name','agent_phone', 'garage_name', 'garage_phone', 'googleFolder', 'images']
    column_labels = dict(license_number='מספר רישוי', car_type="סוג רכב/דגם הרכב", apriser_name = "שם השמאי", playce_of_check='מקום הבדיקה', date_of_entertainment = 'תאריך הארוע', date_of_check = 'תאריך בדיקה הרכב', name_insurance = 'חברת הבדיקה', agent_name = 'שם מבוטח', agent_phone = 'פלאפון מבוטח', garage_name = 'שם הםוכן', garage_phone = 'פלאפון הםוכן', googleFolder = 'Google Folder', images= 'תמונות')
    column_editable_list = ['license_number',  'apriser_name', 'name_insurance']
    column_searchable_list = column_editable_list
    column_formatters = {
        'images': _image_formatter,
    }
    #column_select_related_list = ('images')


