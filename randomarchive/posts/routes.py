# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from randomarchive import db, mysql
from randomarchive.models import User
from randomarchive.posts.forms import PostForm
from randomarchive.config import Config
import MySQLdb.cursors

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        sql_insert_query = '''INSERT INTO post (title,content,author,user_id) VALUES (%s,%s,%s,%s)'''
        print(current_user)
        insert_tuple = (form.title.data,form.content.data,current_user,current_user.id)
        cur.execute(sql_insert_query,insert_tuple)
        mysql.connection.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    print(post_id)
    cur = mysql.connection.cursor()
    sql_select_query = '''SELECT * FROM post WHERE id=%s'''
    select_tuple = (str(post_id))
    cur.execute(sql_select_query, [select_tuple])
    results = cur.fetchall()
    if len(results) == 0:
        abort(404)
    user = User.query.filter_by(id=results[0]['user_id']).first()
    results[0]['author.username'] = user.username
    results[0]['author.email'] = user.email
    results[0]['author.image_file'] = 'https://storage.googleapis.com/' + Config.GCS_BUCKET_NAME + '/' + user.image_file + '?cloudshell=true&orgonly=true&supportedpurview=organizationId'
    return render_template('post.html', title=results[0]['title'], post=results[0])


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    cur = mysql.connection.cursor()
    sql_select_query = '''SELECT * FROM post WHERE id=%s'''
    select_tuple = (str(post_id))
    cur.execute(sql_select_query,[select_tuple])
    results = cur.fetchall()
    if len(results) == 0:
        abort(404)
    if str(results[0]['user_id']) != str(current_user.id):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        sql_update_query = '''UPDATE post SET title=%s, content=%s WHERE id=%s'''
        update_tuple = (form.title.data,form.content.data,str(post_id))
        cur.execute(sql_update_query,update_tuple)
        mysql.connection.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=results[0]['id']))
    elif request.method == 'GET':
        form.title.data = results[0]['title']
        form.content.data = results[0]['content']
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST','GET'])
@login_required
def delete_post(post_id):
    cur = mysql.connection.cursor()
    sql_select_query = '''SELECT * FROM post WHERE id=%s'''
    select_tuple = (str(post_id))
    cur.execute(sql_select_query,[select_tuple])
    results = cur.fetchall()
    if len(results) == 0:
        abort(404)
    if str(results[0]['user_id']) != str(current_user.id):
        abort(403)
    sql_delete_query = '''DELETE FROM post WHERE id=%s'''
    delete_tuple = (str(post_id))
    cur.execute(sql_delete_query, [delete_tuple])
    mysql.connection.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
