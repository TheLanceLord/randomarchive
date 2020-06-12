from flask import render_template, request, Blueprint
from randomarchive.main.forms import SearchForm
from randomarchive.models import User
from randomarchive import db, mysql
from randomarchive.config import Config
import MySQLdb.cursors

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    cur = mysql.connection.cursor()
    sql_select_query = """SELECT * FROM post ORDER BY date_posted DESC"""
    cur.execute(sql_select_query)
    results = cur.fetchall()
    page = 1
    page_num = 1
    results_per_page = 5
    for result in results:
        user = User.query.filter_by(id=result['user_id']).first()
        result['author.username'] = user.username
        result['author.email'] = user.email
        result['author.image_file'] = 'https://storage.googleapis.com/' + Config.GCS_BUCKET_NAME + '/' + user.image_file + '?cloudshell=true&orgonly=true&supportedpurview=organizationId'
        if results_per_page == 0:
            page_num = page_num + 1 
        result['page'] = page_num
        results_per_page = results_per_page - 1
    #print(str(results[0]['title']))
    #print(str(page_num))
    #print(str(page))
    return render_template('home.html', posts=results, pages=page_num+1, page=page)


@main.route("/about")
def about():
    architecture_diagram = 'https://storage.googleapis.com/' + Config.GCS_BUCKET_NAME + '/RandomArchive%20Architecture.jpg?cloudshell=true&orgonly=true&supportedpurview=organizationId'
    return render_template('about.html', title='About', arch_diagram=architecture_diagram)


@main.route("/search")
def search():
    searchterm = request.args['search']
    return search_posts(searchterm)


@main.route("/<string:searchterm>")
def search_posts(searchterm):
    searchform = SearchForm()
    page = request.args.get('page', 1, type=int)
    sql_select_query = '''SELECT * FROM post WHERE title LIKE %s OR content LIKE %s OR user_id LIKE %s ORDER BY post.date_posted DESC'''
    wild_search = '%' + searchterm + '%'
    select_tuple = (wild_search, wild_search, wild_search)
    cur = mysql.connection.cursor()
    cur.execute(sql_select_query, select_tuple)
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
    return render_template('search_posts.html', posts=results, searchterm=searchterm, pages=page_num+1, page=page, total=len(results))
