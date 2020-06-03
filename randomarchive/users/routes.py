from flask import render_template, url_for, flash, redirect, request, Blueprint, Flask, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from randomarchive import db, bcrypt, mysql
from randomarchive.models import User
from randomarchive.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from randomarchive.users.utils import save_picture
import MySQLdb.cursors
from randomarchive.config import Config

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if 'bobbytables' in form.username.data:
            abort(403)
        if 'bobbytables' in form.email.data:
            abort(403)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        default_picture = 'default.jpg'
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file=default_picture)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        payload = json.loads(request.data)
        if 'bobbytables' in payload["username"]:
            abort(403)
        if 'bobbytables' in payload["email"]:
            abort(403)
        hashed_password = bcrypt.generate_password_hash(payload["password"]).decode('utf-8')
        default_picture = '/default.jpg'
        user = User(username=payload["username"], email=payload["email"], password=hashed_password, image_file=default_picture)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if 'bobbytables' in form.email.data:
            abort(403)
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if 'bobbytables' in form.username.data:
            abort(403)
        if 'bobbytables' in form.email.data:
            abort(403)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = 'https://storage.cloud.google.com/' + Config.GCS_BUCKET_NAME + '/' + destination_blob_name + '?cloudshell=true&orgonly=true&supportedpurview=organizationId'
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    cur = mysql.connection.cursor()
    sql_select_query = '''SELECT * FROM post WHERE user_id=%s ORDER BY date_posted DESC'''
    select_tuple = (str(user.id))
    cur.execute(sql_select_query,[select_tuple])
    results = cur.fetchall()
    page_num = 1
    results_per_page = 5
    for result in results:
        user = User.query.filter_by(id=result['user_id']).first()
        result['author.username'] = user.username
        result['author.email'] = user.email
        result['author.image_file'] = 'https://storage.cloud.google.com/' + Config.GCS_BUCKET_NAME + '/' + user.image_file + '?cloudshell=true&orgonly=true&supportedpurview=organizationId'
        if results_per_page == 0:
            page_num = page_num + 1 
        result['page'] = page_num
        results_per_page = results_per_page - 1
    return render_template('user_posts.html', posts=results, user=user, page=page, pages=page_num+1, total=len(results))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
