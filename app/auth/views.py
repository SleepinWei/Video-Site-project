from flask import render_template,redirect,request,url_for,flash
from flask.globals import current_app
from flask_migrate import current
from . import auth
from .. import db
from flask_login import login_user,logout_user,login_required,current_user
from ..models import User
from .forms import LoginForm, RegistrationForm,ChangePassword,ChangeEmail, ResetPassword
from app.emailDev import send_email

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed',user=current_user))
            
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html',user=current_user)

@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account!")
    else:
        flash("Confirmation link is invalid!")
    return redirect(url_for("main.index",user=current_user))

@auth.route("/confirm")
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account',
    'auth/email/confirm',user=current_user,token=token)
    flash("A new confirmation email has been sent to your email")
    return redirect(url_for('main.index',user=current_user))

@auth.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        # 用户访问未授权URL会显示登录表单，FLASH将原地址保存在next参数中，因此能直接跳转
        flash("Invalid username or password",category="err")
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("main.index"))

@auth.route("/register",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.check.data == True:
            user = User(name=form.name.data,password=form.password.data,email=form.email.data,phone=form.phone.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email,'Confirm Your Account',
            'auth/email/confirm',user=user,token=token)
            flash("A confirmation email has been sent to you by email.",category="ok")
            # flash("Sucessful registeration!",category="ok")
            return redirect(url_for('auth.login'))
        else:
            #请加入必须同意用户协议才能注册的逻辑
            flash('Please check the agreement and agree',category="err")
    return render_template("auth/newregister.html",form=form)


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
