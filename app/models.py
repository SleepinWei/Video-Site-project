from app import db

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
import os

from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint


#假想role
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    user = db.relationship('User', backref='role')

#假想user
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(32), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    likes = db.relationship('Videolike',backref='user')
    comments = db.relationship('Comment', backref='user')
    videocols = db.relationship('Videocol', backref='user')
    videos = db.relationship('Video', backref='user')
    def __repr__(self):
        return "<User %r>" % self.name

#假想barrage(弹幕)
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
