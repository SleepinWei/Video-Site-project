from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.utils import login_required
from flask_migrate import current
from flask_login import current_user
from flask import request
from werkzeug.urls import url_decode
from werkzeug.utils import redirect
from app.main.forms import CommentForm, EditProfileForm, RedirectToEditForm,createModule
from . import main
import flask
# from ..models import User
# from ..models import Video
from ..models import *

@main.route('/',methods=["POST","GET"])
def index():
    videos = Video.query.order_by(Video.playnum)
    if(videos.count()>10):
        videos = videos[0:10]
    else:
        videos = videos.all()
    if current_user.is_anonymous:
        return render_template('newerindex.html',user=None,video=videos)
    return render_template('newerindex.html',user=current_user,videos=videos)

# 轮播图
@main.route('/animation/')
def animation():
    data = Video.query.all()
    return render_template('animation.html', data=data)


@main.route('/space',methods=["POST","GET"])
def spaceDefault():
    #if user is not logged in, redirect to login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    #if user is logged in, render the space page
    return flask.render_template('UserSpace.html', user=current_user)

# Default space
@main.route('/space/',methods=["POST","GET"])
def spaceDefaultAddition():
    #the same as above
    #if user is not logged in, redirect to login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    #if user is logged in, render the space page
    return flask.render_template('UserSpace.html', user=current_user)

# Redirect to user space
@main.route('/space/<username>',methods=["POST","GET"])
@login_required
def spaceUser(username):
    #get the user from the database
    if username is '':
        return redirect("auth.login")
    user1=User(username)

    #if click the edit button, redirect to edit page
    form=RedirectToEditForm()
    if form.validate_on_submit():
        return flask.redirect(flask.url_for('editProfile'))
    return flask.render_template('UserSpace.html',user=user1)

@main.route('/video/<videoname>',methods=["POST","GET"])
def playvideo(videoname):
    # video1=Video(videoname)
    video = Video.query.filter_by(title=videoname).first()
    # 这里依据名字从查找video，后期可以改为依据id查找

    form = CommentForm()
    buttonforms = createModule() #button forms 4 in 1 
    # like,coin,star,share
    
    if form.validate_on_submit():
        if current_user.is_anonymous or not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        comment = Comment(content=form.body,user_id=current_user.id,
                video_id=video.id)
        # _get_current_object() returns somethign in the session, and even if author is not declared, this stil works
        # very mysterious and don't konw why
        db.session.add(comment)
        return redirect(url_for('.playvideo'),videoname=videoname)

    if buttonforms[0].validate_on_submit():
        # like
        exist_videolike = Videolike.query.filter_by(user_id=current_user.get_id(),video_id=video.id).first()
        if exist_videolike == None:
            video.likenum += 1 
            videolike = Videolike(video_id=video.id,user_id=current_user.get_id())
            db.session.add(videolike)
        else:
            video.likenum -= 1
            db.session.delete(exist_videolike)
        db.session.commit()

    if(buttonforms[1].validate_on_submit()):
        # coin
        exist_videocoin = Videocoin.query.filter_by(user_id=current_user.get_id(),video_id=video.id).first()
        if exist_videocoin == None:
            video.coinnum += 1
            videocoin = Videocoin(video_id=video.id,user_id=current_user.get_id())
            db.session.add(videocoin)    
            db.session.commit()
        else:
            flash('You have throwed the coin')            

    if(buttonforms[2].validate_on_submit()):
        # star 
        exist_videocol = Videocol.query.filter_by(user_id=current_user.get_id(),video_id=video.id).first()
        if exist_videocol == None:
            video.videocols += 1
            videocol = Videocol(video.id,current_user.get_id())
            db.session.add(videocol)
        else:
            db.session.delete(exist_videocol)
        db.session.commit()

    if(buttonforms[3].validate_on_submit()):
        # share
        pass
        
    
    comments = Comment.query.order_by(Comment.addtime.desc()).all()
    
    # return flask.render_template('extend.html',video=video1)
    return render_template('video.html',video=video,comments=comments, \
    buttonforms=buttonforms,user=current_user,form=form)

# 用户资料编辑
@main.route("/editProfile",methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickName = form.nickName.data
        current_user.password = form.password.data
        current_user.about_me = form.introduction.data

        db.session.add(current_user)
        flash("You have updated your profile")
        return redirect(url_for(".spaceUser",username=current_user.name))
    form.nickName.data = current_user.nickName
    form.password.data = current_user.password
    form.introduction.data = current_user.introduction
    return render_template('EditProfile.html',form=form)

# 隐私政策
@main.route('/privacy')
def privacy():
    return flask.render_template('privacy.html')

#用户协议
@main.route('/term_of_use')
def licence():
    return flask.render_template('termOfUse.html')

# 管理员资料编辑器
