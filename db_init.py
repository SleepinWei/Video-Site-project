
# deprecated -- zyw 
# can't operate on db if app is not initialized 
# this file is useless 

from app import db
from app.models import  Video,User
from datetime import datetime

# db.create_all()
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

def create_user(username):
    user = User(name=username)
    user.last_seen = datetime.utcnow()

    db.session.add(user)
    db.session.commit()

if __name__ == "__main__":
    add_video("Never Gonna Give You Up","A Song",12)