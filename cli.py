from datetime import datetime
import logging
import click
from app.models import User,Video
from app import db

def register(app):
    @app.cli.command("create_user")
    @click.argument("username")
    def create_user(username):
        user = User(name=username)
        db.session.add(user)
        db.session.commit()
        
    @app.cli.command("create_videocol")
    @click.argument("userid")
    @click.argument("videoid")
    def create_videocol(userid,videoid):
        videocol = Videocol(videoid, userid)
        db.session.add(videocol)
        db.session.commit()

    @app.cli.command("create_role")
    @click.argument("rolename")
    def create_role(rolename):
        role = Role(name=rolename)
        db.session.add(role)
        db.session.commit()

    @app.cli.command("add_video")
    @click.argument("video_title")
    @click.argument("video_info")
    @click.argument("video_likenum")
    def add_video(video_title,video_info,video_likenum):
        video = Video(title=video_title,
        info=video_info,playnum=0,likenum=0,commentnum=0,
        collectionnum=0,coinnum=0,
        length=0,danmu_path=None,uploaduser_id=None)

        video.url = "static/video/"+video_title+".mp4"
        video.thumbnail = "/static/images/thumbnail/"+video.title+".jpg"
        video.uploadtime = datetime.utcnow()

        db.session.add(video)
        db.session.commit()
