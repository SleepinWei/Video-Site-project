from app import db
from app.models import  Video,User
import datetime

# db.create_all()
def add_video(video_title,video_info,video_likenum):
    video = Video(title=video_title,likenum=video_likenum,info=video_info)
    video.url = "static/video/"+video_title+".mp4"
    video.thumbnail = "/static/images/thumbnail/"+video.title
    video.uploadtime = datetime.utcnow()

    db.session.add(video)
    db.session.commit()

def create_user(username):
    user = User(name=username)
    user.last_seen = datetime.utcnow()

    db.session.add(user)
    db.session.commit()

if __name__ == "__main__":
    add_video("")