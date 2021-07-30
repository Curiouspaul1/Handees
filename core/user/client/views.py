from . import client
from flask import request
from sqlalchemy.exc import IntegrityError
from core import db
from core.models import User


@client.route("/")
def register():
    # get data
    data_ = request.get_json(force=True)
    new_user = User()
    for key, value in data_.items():
        new_user.key = value
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        return {
            "ok": False,
            "msg": "User with email or telephone already exists"
        }, 401
    return {
        "ok": True,
        "msg": "Registered user successfully"
    }, 200
