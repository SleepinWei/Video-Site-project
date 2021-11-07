from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tony@localhost/testuser"
app.debug = True
db = SQLAlchemy(app)


class UserExistError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    userid = db.Column(db.String(16), primary_key=True)
    pw_hash = db.Column(db.Unicode(160), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    vipgroup = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    # add new things here

    def __repr__(self) -> str:
        return "<User-%s>" % self.username


def create_user(name: str, plain_pw: str) -> User:
    if User.query.filter_by(username=name).first():
        raise UserExistError("User '%s' already exists" % name)
    u = User(username=name, vipgroup="normal")
    slt = os.urandom(32)
    pwd = hashlib.pbkdf2_hmac('sha256', plain_pw.encode(
        'utf-8'), slt, 100000, dklen=128)
    u.pw_hash = (slt + pwd).decode('latin1')
    m = hashlib.md5()
    m.update(('%s [ %s' % (name, datetime.now().ctime())).encode('utf-8'))
    u.userid = str(int(m.hexdigest(), 16))[0:8]
    # TODO : handle userid conflict
    return u


def check_user_pw(name: str, plain_pw: str) -> bool:
    x = User.query.filter_by(username=name).first()
    slt = bytes(x.pw_hash[:32], 'latin1')
    pwd = hashlib.pbkdf2_hmac('sha256', plain_pw.encode(
        'utf-8'), slt, 100000, dklen=128)
    return (slt + pwd).decode('latin1') == x.pw_hash

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    u = create_user("testuser", "tony318")
    db.session.add(u)
    print(check_user_pw("testuser", "tony318"))
    db.session.commit()
