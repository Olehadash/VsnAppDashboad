
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from VsnAppDashboad import db
from datetime import datetime, date
import random
import string

InventID = 0

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

image_session = db.Table(
    'image_session',
    db.Column('session_id', db.Integer(), db.ForeignKey('session.id')),
    db.Column('imageslink_id', db.Integer(), db.ForeignKey('imageslink.id'))
)



class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.Integer)
    car_type = db.Column(db.String(255))
    apriser_name = db.Column(db.String(255))
    playce_of_check = db.Column(db.String(255))
    date_of_entertainment = db.Column(db.DateTime())
    date_of_check = db.Column(db.DateTime())
    name_insurance = db.Column(db.String(255))
    agent_name = db.Column(db.String(255))
    agent_phone = db.Column(db.String(255))
    garage_name = db.Column(db.String(255))
    garage_phone = db.Column(db.String(255))
    googleFolder = db.Column(db.String(255))
    images = db.relationship('Session', secondary=image_session,
                            backref=db.backref('session', lazy='dynamic'))
    

    def __str__(self):
        return self.id


class Imageslink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255))
    

    def __str__(self):
        return self.link