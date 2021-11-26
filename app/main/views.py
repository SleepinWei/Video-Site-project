from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.utils import login_required
from flask_migrate import current
from flask_login import current_user
from werkzeug.urls import url_decode
from werkzeug.utils import redirect
from app.main.forms import CommentForm, EditProfileForm
from . import main
import flask
# from ..models import User
# from ..models import Video
from ..models import *

@main.route('/<int:page>/')
def index(page=None):
    if page is None:
        page = 1
    tags = Tag.query.all()
    page_data = Movie.query
    # 标签（eg 美食、电竞……）
    tid = request.args.get('tid', 0)  # 获取tid，获取不到返回0
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    # 视频受欢迎度
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 视频发布时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    # 播放量
    pm = request.args.get('pm', 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    # 评论量
    cm = request.args.get('cm', 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )

    page = request.args.get("page", 1)
    page_data = page_data.paginate(page=int(page), per_page=10)

    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    return render_template("index.html", tags=tags, p=p, page_data=page_data)

# 轮播图
@home.route('/animation/')
def animation():
    data = Preview.query.all()
    return render_template('animation.html', data=data)


@main.route('/space')
def spaceDefault():
    #if user is not logged in, redirect to login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    #if user is logged in, render the space page
        return flask.render_template('UserSpace.html', user=current_user)

# Default space
@main.route('/space/')
def spaceDefaultAddition():
    #the same as above
    #if user is not logged in, redirect to login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    #if user is logged in, render the space page
        return flask.render_template('UserSpace.html', user=current_user)

# Redirect to user space
@main.route('/space/<username>')
@login_required
def spaceUser(username):
    #get the user from the database
    user1=User(username)

    return flask.render_template('UserSpace.html',user=user1)

@main.route('/video/<videoname>')
def playvideo(videoname):
    # video1=Video(videoname)
    video = Video.query.filter_by(title=videoname).first()
    # 这里依据名字从查找video，后期可以改为依据id查找

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.body,author=current_user._get_current_object())
        # _get_current_object() returns somethign in the session, and even if author is not declared, this stil works
        # very mysterious and don't konw why
        db.session.add(comment)
        return redirect(url_for('.playvideo'),videoname=videoname)
    comments = Comment.query.order_by(Comment.addtime.desc()).all
    
    # return flask.render_template('extend.html',video=video1)
    return render_template('video.html',video=video,comments=comments )

@main.route("/edit-profile",methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickName = form.nickName.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("You have updated your profile")
        return redirect(url_for(".spaceUser",username=current_user.name))
    form.nickName.data = current_user.nickName
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)

# 管理员资料编辑器
