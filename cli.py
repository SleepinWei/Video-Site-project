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
    
    @app.cli.command("add_video")
    @click.argument("video_title")
    @click.argument("video_info")
    @click.argument("video_likenum")
    def add_video(video_title,video_info,video_likenum):
        video = Video(title=video_title,likenum=video_likenum,info=video_info)
        video.url = "/video/"+video_title
        video.thumbnail = "/static/images/thumbnail/"+video.title
        video.uploadtime = datetime.utcnow()

        db.session.add(video)
        db.session.commit()