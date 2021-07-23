from core.extensions import db
from datetime import datetime as d

# Base class
class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)


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




    