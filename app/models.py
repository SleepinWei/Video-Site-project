# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy.orm import backref
# from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint

from . import db
from datetime import datetime
import os, hashlib
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


#假想role
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    user = db.relationship('User', backref='role')

#user需要增加：coins，level(等级), levelProgress（等级进度，直接用0-100就行，简单点）, role_id需要知道对应关系
#假想user
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    nickName = db.Column(db.String(64),unique=True)
    pw_hash = db.Column(db.String(128), unique=True)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id')) #？对应关系，至少需要VIP、普通用户
    likes = db.relationship('Videolike',backref='user')
    comments = db.relationship('Comment', backref='user')
    videocols = db.relationship('Videocol', backref='user')
    videos = db.relationship('Video', backref='user')
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    def __repr__(self):
        return "<User %r>" % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self,password):
        self.pw_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.pw_hash,password)

    def ping(self):
        # 上次登录时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)
#假想barrage(弹幕)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Barrage(db.Model):
    __tablename__ = 'barrage'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(127))
    video_id = db.Column(db.Integer,db.ForeignKey('video.id'))

# 视频
class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)  # 编号（主键）
    title = db.Column(db.String(255), unique=True)  # 视频标题
    url = db.Column(db.String(255), unique=True)  # 地址 即视频对应跳转的url_for
    info = db.Column(db.Text)  # 简介
    playnum = db.Column(db.BigInteger)  # 播放量
    likenum = db.Column(db.BigInteger)  # 点赞数
    commentnum = db.Column(db.BigInteger)  # 评论数
    length = db.Column(db.String(100))  # 视频时长
    uploadtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 视频上传时间
    uploaduser_id = db.Column(db.Integer, db.ForeignKey('user.id'))    # 上传的user外键
    videolikes = db.relationship("Videolike", backref='video')  #点赞外键关联
    comments = db.relationship("Comment", backref='video')  # 评论外键关联
    videocols = db.relationship("Videocol",backref='video') # 收藏外键关联
    barrages = db.relationship("Barrage", backref='video')   # 弹幕外键关联
    def __init__(self,title,url,info,playnum,likenum,commentnum,length,uploaduser_id):
        self.title = title
        self.url = url
        self.info = info
        self.playnum = playnum
        self.likenum = likenum
        self.commentnum = commentnum
        self.length = length
        self.uploaduser_id = uploaduser_id
    def __repr__(self):
        return "<Video %r>" % self.id

 
# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))  # 所属视频
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    # username = db.Column(db.String,db.ForeignKey('user.nickName'))

    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 发言时间
    def __init__(self,content,video_id,user_id):
        self.content = content
        self.video_id = video_id
        self.user_id = user_id
    def __repr__(self):
        return "<Comment %r>" % self.id


# 视频收藏
class Videocol(db.Model):
    __tablename__ = 'videocol'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))  # 所属视频
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    def __init__(self,video_id,user_id):
        self.video_id = video_id
        self.user_id = user_id

    def __repr__(self):
        return "<Videocol %r>" % self.id

# 视频点赞
class Videolike(db.Model):
    __tablename__ = 'videolike'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))  # 所属视频
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    def __init__(self,video_id,user_id):
        self.video_id = video_id
        self.user_id = user_id
    def __repr__(self):
        return "<Videolike %r>" % self.id

# ---------------------------#
# 用户操作接口
class UserExistError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

# 新建用户，以名字，明文密码
# 对已存在抛出UserExistError
def create_user(nm: str, plain_pw: str) -> User:
    if User.query.filter_by(name=nm).first():
        raise UserExistError("User '%s' already exists" % nm)
    u = User(name=nm, role_id=1)    # 默认role
    slt = os.urandom(32)
    pwd = hashlib.pbkdf2_hmac('sha256', plain_pw.encode(
        'utf-8'), slt, 100000, dklen=128)
    u.pw_hash = (slt + pwd).decode('latin1')
    return u

# 检查用户密码
# 对用户不存在抛出UserNotFoundError
def check_user_pw(nm: str, plain_pw: str) -> bool:
    x = User.query.filter_by(name=nm).first()
    if not x:
        raise UserNotFoundError("User '%s' not found" % nm)
    slt = bytes(x.pw_hash[:32], 'latin1')
    pwd = hashlib.pbkdf2_hmac('sha256', plain_pw.encode(
        'utf-8'), slt, 100000, dklen=128)
    return (slt + pwd).decode('latin1') == x.pw_hash
# ---------------------------#


#测试
if __name__ == '__main__':
    '''创建表'''
    db.drop_all()
    db.create_all()
    '''实例化'''
    role1 = Role(name='admin')
    role2 = Role(name='guest')
    db.session.add(role1)
    db.session.add(role2)
    db.session.commit()   
    
    user1 = User(name='Oscar',password='123456',role_id=role1.id)
    user2 = User(name='Peter',password='ggggbaby',role_id=role2.id)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    temp_video = Video('大碗宽面','100.0.0.5000','庆祝吴签入狱',999,777,99,'00:12:13',user1.id)
    db.session.add(temp_video)
    db.session.commit()
    temp_comment = Comment('edg牛逼！！',temp_video.id,(User.query.filter_by(name='Oscar').first()).id)
    temp_col = Videocol(temp_video.id,user2.id)
    temp_like = Videolike(Video.query.filter_by(likenum=777).first().id,user2.id)
    db.session.add_all([temp_col,temp_comment,temp_like])
    db.session.commit()
#    app.run()
