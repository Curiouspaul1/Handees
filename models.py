from core.extensions import db
from flask import current_app
from datetime import datetime as d

# Base class
class Base(db.Model):
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


class User(Base):
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    signup_date = db.Column(db.DateTime, default=d.utcnow())
    profile_photo = db.Column(db.String(200))
    telephone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(100))
    is_handyman = db.Column(db.Boolean, default=False)
    personal_id = db.Column(db.String(200))

    def __init__(self) -> None:
        super().__init__()
        if self.role is None:
            if self.email in current_app.config['ADMIN_EMAILS']:
                self.role = Role.query.filter_by(name='admin').first()
            if self.role is None:
                if self.is_handyman:
                    self.role = Role.query.filter_by(name='handyman').first()
                else:
                    self.role = Role.query.filter_by(default=True).first()
    
    # permission helper methods
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_admin(self):
        return self.can(PERMISSIONS.ADMIN)
                

class Role(Base):
    name = db.Column(db.String(50))
    is_default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
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
            role = Role.query.filter_by(name=role).first()
            if role is None:
                role = Role(name=item)
            role.reset_permissions()
            # add permissions for given role
            for perm in roles[item]:
                role.add_permission(perm)
            # set as default role if name matches default_role 
            role.is_default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()



    