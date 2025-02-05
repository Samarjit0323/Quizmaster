from flask import render_template, url_for, flash, redirect, Blueprint, request
from app.users.forms import regForm, loginForm, updateProfile
from app import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from app.users.utils import save_picture
from app.models import User

users = Blueprint('users', __name__)

@users.route("/register",methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    reg1=regForm()
    if reg1.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reg1.password.data).decode('utf-8')
        new_user= User(username=reg1.username.data,email=reg1.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit() 
        flash(f'Account created for {reg1.username.data}!',category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register',form=reg1)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    log1=loginForm()
    if log1.validate_on_submit(): 
        new_user=User.query.filter_by(email=log1.email.data).first()
        if new_user and bcrypt.check_password_hash(new_user.password, log1.password.data):
            login_user(new_user,remember=log1.remember.data)
            flash('Login Successful', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Retry Login', 'danger')
    return render_template('login.html', title='Login',form=log1)

@login_required
@users.route("/profile")
def profile():
    if current_user.is_authenticated:
        image_file=url_for('static', filename=f'DPs/{current_user.pro_img}')
        return render_template('profile.html', title='Profile', img=image_file,  username=current_user.username, category=current_user.category, max_score=current_user.max_score)
    flash("Please Log In/Register to continue!","warning")
    return redirect(url_for("users.login"))
@login_required
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@login_required
@users.route("/update_profile",methods=['GET', 'POST'])
def updtProfile():
    if current_user.is_authenticated:
        form=updateProfile()
        if form.validate_on_submit():
            current_user.username=form.username.data
            current_user.email=form.email.data
            if form.profile_pic.data: 
                pic_file=save_picture(form.profile_pic.data)
                current_user.pro_img=pic_file
            db.session.commit()
            flash('Profile Updated', 'success')
            return redirect(url_for('users.profile'))
        elif request.method=='GET':
            #populate form fields with current user details if no data is submitted yet i.e. missing POST request
            form.username.data=current_user.username
            form.email.data=current_user.email
        return render_template('update_profile.html', title='Update Profile', form=form)
    flash("Please Log In/Register to continue!","warning")
    return redirect(url_for("users.login"))