from geoalchemy2.exc import GeoAlchemyError
from sqlalchemy.orm import backref
from flask import current_app
from datetime import datetime as d
from geoalchemy2 import Geometry
from core.extensions import db


# Base class
class Base:
    id = db.Column(db.Integer, primary_key=True, nullable=False)

# User permissions
class PERMISSIONS:
    # client permissions
    GET_CLIENT = 1
    GIVE_RATING = 2
    POST_GIG = 4
    # handymen permisions
    ACCEPT_GIG = 8
    # admin
    ADMIN = 16


class User(Base, db.Model):
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    signup_date = db.Column(db.DateTime, default=d.utcnow())
    profile_photo = db.Column(db.String(200))
    telephone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(100))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    is_handyman = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    personal_id = db.Column(db.String(200))
    geometry = db.Column(Geometry(geometry_type='POINT', management = True))
    # relationships
    gigs_ = db.relationship('Gig', backref='owner')
    workstatus = db.relationship('Workstatus', backref='user', uselist=False)
    kin = db.relationship('User', backref='user', uselist=False)

    def __init__(self) -> None:
        super().__init__()
        if self.role is None:
            if self.email in current_app.config['ADMIN_EMAILS']:
                self.role = Role.query.filter_by(role_name='admin').first()
            if self.role is None:
                if self.is_handyman:
                    self.role = Role.query.filter_by(role_name='handyman').first()
                    self.add_workstatus()
                else:
                    self.role = Role.query.filter_by(default=True).first()
    
    # permission helper methods
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_admin(self):
        return self.can(PERMISSIONS.ADMIN)
    
    def contact_info(self):
        return {
            "telephone": self.telephone,
            "address": self.address,
            "email": self.email
        }

    def verify_email(self):
        if self.verify_email is False:
            self.verify_email = True
            db.session.commit()
        return self.verify_email
    
    def add_workstatus(self):
        self.workstatus = Workstatus()
    
    # def update_work_status(self):
         

class Role(Base, db.Model):
    role_name = db.Column(db.String(50))
    is_default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    # relationships
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self) -> None:
        super().__init__()
        if self.permissions is None:
            self.permissions = 0
    
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    def reset_permissions(self):
        self.permissions = 0

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    @staticmethod
    def add_roles():
        roles = {
            'client': [PERMISSIONS.GET_CLIENT, PERMISSIONS.GIVE_RATING, PERMISSIONS.POST_GIG],
            'handyman': [PERMISSIONS.ACCEPT_GIG],
            'admin': [PERMISSIONS.ADMIN]
        }
        default_role = 'client'
        for item in roles:
            role = Role.query.filter_by(role_name=role).first()
            if role is None:
                role = Role(role_name=item)
            role.reset_permissions()
            # add permissions for given role
            for perm in roles[item]:
                role.add_permission(perm)
            # set as default role if name matches default_role 
            role.is_default = (role.role_name == default_role)
            db.session.add(role)
        db.session.commit()


class Gig(Base, db.Model):
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    glat = db.Column(db.Float)
    glon = db.Column(db.Float)
    gig_geometry = db.Column(Geometry(geometry_type='POINT', management = True))
    date_created = db.Column(db.DateTime(), default=d.utcnow())


class Workstatus(Base, db.Model):
    time_of_departure = db.Column(db.DateTime(), default=d.utcnow())
    current_lon = db.Column(db.Float)
    current_lat = db.Column(db.Float)
    destination_lon = db.Column(db.Float)
    destination_lat = db.Column(db.Float)
    completed_task = db.Column(db.Boolean, default=False)
    time_of_completion = db.Column(db.DateTime())
    arrived_home = db.Column(db.Boolean)
    time_of_home_arrival = db.Column(db.DateTime())


class Kin(Base, db.Model):
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    address = db.Column(db.String(100))
