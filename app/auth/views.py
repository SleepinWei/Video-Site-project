from flask import render_template,redirect,request,url_for,flash
from flask.globals import current_app
from flask_migrate import current
from . import auth
from .. import db
from flask_login import login_user,logout_user,login_required,current_user
from ..models import User
from .forms import LoginForm, RegistrationForm,ChangePassword,ChangeEmail, ResetPassword

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        # 用户访问未授权URL会显示登录表单，FLASH将原地址保存在next参数中，因此能直接跳转
        flash("Invalid username or password")
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("main.index"))

@auth.route("/register")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.check.data == True:
            user = User(name=form.name.data,password=form.password.data,email=form.email.data,phone=form.phone.data)
            db.session.add(user)
            flash("Sucessful registeration!")
            return redirect(url_for('auth.login'))
        else:
            #请加入必须同意用户协议才能注册的逻辑
            flash('Please check the agreement and agree')
    return render_template("auth/register.html",form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)



@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPassword()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data.lower()).first()
    #     if user:
    #         token = user.generate_reset_token()
    #         send_email(user.email, 'Reset Your Password',
    #                    'auth/email/reset_password',
    #                    user=user, token=token)
    #     flash('An email with instructions to reset your password has been '
    #           'sent to you.')
    #     return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
