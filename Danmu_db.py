from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

class Config:
    '''配置个人参数'''
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "DFVBNL"

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
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
    videos = db.relationship('Video', backref='user')
    videos = db.relationship('Video', backref='user')
    def __repr__(self):
        return "<User %r>" % self.name
# 视频（by wwx）
class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)  # 编号（主键）
    title = db.Column(db.String(255), unique=True)  # 视频标题
    url = db.Column(db.String(255), unique=True)  # 地址 即视频对应跳转的url_for
    info = db.Column(db.Text)  # 简介
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论数
    length = db.Column(db.String(100))  # 视频时长
    uploadtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 视频上传时间
    uploaduser_id = db.Column(db.Integer, db.ForeignKey('user.id'))    # 上传的user外键
    danmus = db.relationship("Danmu", backref='video')   # 弹幕外键关联
    def __init__(self,title,url,info,playnum,commentnum,length):
        self.title = title
        self.url = url
        self.info = info
        self.playnum = playnum
        self.commentnum = commentnum
        self.length = length
    def __repr__(self):
        return "<Video %r>" % self.id

###############   new  start  ##################
    def list_Danmu(self):
        d=self.query.get(self.id)
        for i in d.danmus:
            print(i.danmu_id,i.content,"video_id:",i.video_id,"发布者",i.submitter,"发布时间",i.starttime)
# 弹幕表
class Danmu(db.Model):
    __tablename__ = 'barrage'
    danmu_id = db.Column(db.Integer, primary_key=True) # 弹幕编号（主键）
    content = db.Column(db.String(127), nullable=False) # 弹幕内容（非空）
    length = db.Column(db.Integer, nullable=False) # 弹幕长度（非空）
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False) # 所属视频编号（非空）
    submitter = db.Column(db.String(63), nullable=False) # 发布者（非空）
    special_color = db.Column(db.Enum("Blue","Red","Yellow","Green")) # 专属颜色（可以为空，普通的黑色）
    starttime = db.Column(db.DateTime, index=True, default=datetime.now)  # 发弹幕时间（建立索引）
    lasttime= db.Column(db.Integer)# 弹幕持续时间，根据长度的某种换算规则？单位：秒
    def query_by_time(self,time):# 某时刻显示的弹幕数量
        lastsecond=timedelta(seconds=self.lasttime)
        d=self.query.filter(time>=self.starttime and time<self.starttime+lastsecond)
        return d
###############   new  end  ##################
# 测试
if __name__ == '__main__':
    '''创建表'''
    db.drop_all()
    db.create_all()
    '''实例化'''
    temp_video = Video('大碗宽面', '100.0.0.5000', '庆祝吴签入狱', 999, 99, '00:12:13')
    db.session.add(temp_video)
    db.session.commit()
    b1=Danmu(content="哈哈哈哈哈",length=len("哈哈哈哈哈"),video_id=temp_video.id, submitter="张三",starttime=datetime(2020, 12, 31, 17, 44, 27, 138000),lasttime=50)
    b2=Danmu(content="嘿嘿嘿",length=len("嘿嘿嘿"),video_id=temp_video.id, submitter="张四",starttime=datetime(2020, 12, 31, 17, 44, 27, 138000),lasttime=1)
    b3=Danmu(content="牛逼",length=len("牛逼"),video_id=temp_video.id, submitter="张四",starttime=datetime(2020, 12, 31, 17, 44, 47, 138000),lasttime=50)
    b4=Danmu(content="爷青回",length=len("爷青回"),video_id=temp_video.id, submitter="张五",starttime=datetime(2020, 12, 31, 17, 44, 37, 138000),lasttime=1)

    db.session.add_all([b1,b2])
    db.session.commit()
    temp_video.list_Danmu()
    print(b4.query_by_time(datetime(2020, 12, 31, 17, 44, 37, 138000)))
    app.run() 