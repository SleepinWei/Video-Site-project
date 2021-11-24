from . import db
# update by wxr:1.User-VIP/VipLevel/update_video 2.Video-collectionnum/danmu_path 3.get_user_space_info/VideoNotFoundError
# collect_video/like_video
# class User:
#    #def __init__(username,NickName, ID, VIP,Level, LevelProgress,    Coins,    Stars,    Introduction):
#    def __init__(self,name):
#        self.NickName=name+'Nick'
#        self.ID=name+'ID'
#        self.VIP=True
#        self.Level=4
#        self.LevelProgress=30
#        self.Coins=10
#        self.Stars=4
#        self.Introduction="23333333"
#        self.FavouriteVideo=[{'name':'v1', 'Information':'i1john','Path':'none'},{'name':'v2', 'Information':'i2john','Path':'none'}]
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint

import os, hashlib

#role
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    user = db.relationship('User', backref='role')

#user
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    pw_hash = db.Column(db.String(32), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    VIP = db.Column(db.Bool)
    VipLevel = db.Column(db.Integer)
    coin = db.Column(db.Integer)
    likes = db.relationship('Videolike',backref='user')
    comments = db.relationship('Comment', backref='user')
    videocols = db.relationship('Videocol', backref='user')
    upload_videos = db.relationship('Video', backref='user')
    def __repr__(self):
        return "<User %r>" % self.name

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
    collectionnum= db.Column(db.BigInteger)  # 收藏数
    length = db.Column(db.String(100))  # 视频时长
    uploadtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 视频上传时间
    danmu_path =db.Column(db.String(100)) # 弹幕表存放路径
    uploaduser_id = db.Column(db.Integer, db.ForeignKey('user.id'))    # 上传的user外键
    comments = db.relationship("Comment", backref='video')  # 评论外键关联
    videoCollect = db.relationship("Videocol",backref='video') # 收藏外键关联
    def __init__(self,title,url,info,playnum,likenum,commentnum,collectnum,length,uploaduser_id,danmu_path):
        self.title = title
        self.url = url
        self.info = info
        self.playnum = playnum
        self.likenum = likenum
        self.commentnum = commentnum
        self.length = length
        self.uploaduser_id = uploaduser_id
        self.collectnum=collectnum
        self.danmu_path=danmu_path

    def __repr__(self):
        return "<Video %r>" % self.id

 
# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))  # 所属视频
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
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

def get_user_space_info(username):
    user = User.query.filter_by(name=username).first()
    if not user:
        raise UserNotFoundError("User '%s' not found" % username)
    return user

class VideoNotFoundError(Exception):
    pass

# 点赞视频
def like_video(video_id):
    video = Video.query.filter_by(id=video_id).first()
    if not video:
        raise VideoNotFoundError("Video '%s' not found" % video_id)
    video.update({'likenum':video.likenum+1})
    db.session.commit()

# 收藏/取消收藏视频
def collect_video(video_id, user_id):
    video = Video.query.filter_by(id=video_id).first()
    if not video:
        raise VideoNotFoundError("Video '%s' not found" % video_id)

    newvideo=Videocol(video_id=video_id,user_id=user_id)
    if (newvideo in video.videoCollect):
        Videocol.query.filter(Videocol.video_id==video_id,Videocol.user_id==user_id).delete()
        video.update({'collectionnum': video.collectionnum - 1})
    else:
        video.update({'collectionnum': video.collectionnum + 1})
        db.session.add(newvideo)
    db.session.commit()

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
