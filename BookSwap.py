from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_mail import Mail
from account_management.email import MailManager
from account_management.create_account import validate_email, validate_password
from encryption.encryption import encrypt
from flask.ext.paginate import Pagination
from datetime import timedelta

import json

# Use dbOps to communicate interact with the DB. See operations.py
# to understand what operations are defined
from database.operations import DBOperations as dbOps

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'mcgillbookswap@gmail.com',
    MAIL_PASSWORD = 'ithinkthereforeiam3',
    SECRET_KEY = 'flask+mongoengine=<3',
    SECURITY_PASSWORD_SALT = 'istilllikenodejsmore',
    MONGODB_SETTINGS = {'DB': 'bookswap_development', 'alias':'default', 'port':57589}
)

from database.models import db
db.init_app(app)
# initialize email object
mail = Mail(app)

mail_manager = MailManager(mail, app)


@app.route('/')
def index():
    return render_template('index.html', page='index')


@app.route('/signup')
def signup():
    return render_template('signup.html', page='signup')


@app.route('/confirm', methods=['GET'])
def confirm_email():
    if request.method == 'GET':
        token = request.args.get('token')
        dbOps.confirm_email(token)
        return render_template('index.html', page='index')

@app.route('/create_account', methods=['POST'])
def create_account():
    errors = []
    password = request.form['password']
    email = request.form['email']
    if request.method == 'POST':
        errors = validate_password(password)
        email_errors = validate_email(email)
        if len(email_errors) is not 0:
            errors.append(email_errors)

    if len(errors) is 0:
        if dbOps.user_exists(email):
            flash("Account already exists for this email")
            return render_template('signup.html', error=errors)
        else:
            dbOps.insert_user(email, encrypt(password))
            dbOps.send_verification_email(email, mail_manager)
            return render_template('index.html')
    else:
        formatted_error = '. '.join(str(error) for error in errors)
        flash(formatted_error)
        return render_template('signup.html')


@app.route('/contact_seller', methods=['POST'])
def contact_seller():
    message = request.form['contact_message']
    email = request.form['contact_email']
    user_id = session['user_id']
    dbOps.send_contact_seller_email(email, mail_manager, user_id)
    return redirect(url_for("show_user_page", user_id=user_id))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if len(email) is 0 or len(password) is 0:
            flash("Please provide an email address and a password")
            return render_template("index.html")

        is_valid = dbOps.validate_login_credentials(email, encrypt(password))
        user = dbOps.get_user_by_email(email)
        if is_valid:
            if dbOps.is_user_account_activated(email):
                session['logged_in'] = True
                session['user_id'] = user.user_id
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=20)
                return redirect(url_for('show_user_page', user_id=user.user_id))
            else:
                flash("Your account has not been activated yet. Please follow the URL in your email")
                return render_template("index.html")
        else:
            flash("invalid login credentials")
            return render_template("index.html")


@app.route('/user/<string:user_id>', methods=['GET', 'POST'])
def show_user_page(user_id):
    if request.method == 'GET':
        if not session.get('logged_in'):
            return "You are not logged in"
        user = dbOps.get_user_by_ID(user_id)
        if user:
            sorting = request.args.get('sorting')
            if sorting == 'OldestFirst':
                sorting = 'OldestFirst'
                posts = dbOps.get_oldest_first_posts_by_user(user)
            else:
                sorting = 'MostRecent'
                posts = dbOps.get_most_recent_posts_by_user(user)
            page, per_page, offset = get_page_items(5)
            pagination = Pagination(page=page, total=len(posts), search=False, record_name='posts', per_page=5, css_framework='foundation')
            return render_template('user_page.html', user_id=user_id, posts=posts[offset:offset+per_page], pagination=pagination, sorting=sorting)
        else:
            return "No user account associated with that user"

    if request.method == 'POST':
        return redirect(url_for('create_post', user_id=user_id))

def get_page_items(posts_per_page):
    page = int(request.args.get('page', 1))
    offset = (page - 1) * posts_per_page
    return page, posts_per_page, offset

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if not session.get('logged_in'):
        return 'You are not logged in'
    user_id = request.values['user_id']
    if request.method == 'GET':
        return render_template("create_post_page.html", user_id=session['user_id'])
    else:
        title = request.values['textbook_title']
        author = request.values['textbook_author']
        if not title:
            flash("You need to submit a title for the book")
            return render_template("create_post_page.html")

        newpost = dbOps.insert_post(title, user_id, author)
        return redirect(url_for('show_post', post_id=newpost.post_id, user_id=session['user_id']))

@app.route('/posts', methods=['GET'])
def show_all_posts():
    if not session.get('logged_in'):
        return 'You are not logged in'
    if request.method == 'GET':
        posts = dbOps.get_all_posts()
        page, per_page, offset = get_page_items(20)
        pagination = Pagination(page=page, total=len(posts), search=False, record_name='posts', per_page=per_page, css_framework='foundation')
        return render_template("posts.html", posts=posts[offset:offset+per_page], pagination=pagination, user_id=session['user_id'])

# Routes relating to searching
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form['search']
        posts = dbOps.search(query)
        if posts:
            page, per_page, offset = get_page_items(20)
            pagination = Pagination(page=page, total=len(posts), search=False, record_name='posts', per_page=per_page,
                                    css_framework='foundation')
            return render_template("posts.html", posts=posts[offset:offset + per_page], pagination=pagination, search_terms=query, user_id=session['user_id'])
        else:
            flash("No posts match your search!")
            return redirect(url_for("show_all_posts"))

# Routes relating to searching
@app.route('/search-realtime', methods=['POST'])
def searchWithoutLoading():
    if request.headers['Content-Type'] == 'application/json':
        request_json = request.get_json()
        query = request_json['search_query']
        if len(query) != 0:
            print "Going in here!"
            print query
            posts = dbOps.search(query)

            if len(posts) == 0:
                posts_json = json.dumps({'posts_data': []})
                return posts_json

            formatted_posts = []
            for post in posts:
                new_post = (
                    post.textbook_title,
                    post.textbook_author,
                    str(post.post_id)
                )
                formatted_posts.append(new_post)

            posts_dictionary = {
                'posts_data':
                    list([{
                        'textbook_title': textbook_title,
                        'textbook_author': textbook_author,
                        'post_id': post_id
                    } for (textbook_title, textbook_author, post_id) in formatted_posts])
            }
            print posts_dictionary
            posts_json = json.dumps(posts_dictionary)
            return posts_json
        else:
            print "No posts were found!"
            posts_json = json.dumps({'posts_data': []})
            return posts_json

@app.route('/post/<string:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    if not session.get('logged_in'):
        return 'You are not logged in'
    if request.method == 'GET':
        post = dbOps.get_post(post_id=post_id)
        if post:
            return render_template("post_page.html", user=post.creator, title=post.textbook_title, user_id=session['user_id'])
        else:
            return "The post you are trying to access does not exist"

    if request.method == 'POST':
        creator = dbOps.get_post(post_id=post_id).creator
        dbOps.remove_post(post_id)
        flash("Post deleted successfully")
        return redirect(url_for("show_user_page", user_id=creator.user_id))
    else:
        return 'No other options implemented yet'


@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.pop('logged_in', None)
        return render_template("index.html")

app.secret_key = 'FOX98PPPCATCHER09FREEFLIGHT'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
