from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_mail import Mail
from account_management.token import Token
from account_management.email import MailManager
from account_management.create_account import validate_email, validate_password
from encryption.encryption import encrypt
from flask.ext.paginate import Pagination
from datetime import timedelta

import json

# Use dbOps to communicate interact with the DB. See operations.py
# to understand what operations are defined
from database.operations import DBOperations as dbOps
from database.forms import EditAccountForm, EditPostForm

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
    MONGODB_SETTINGS = {'DB': 'bookswap_development', 'alias':'default', 'port': 57589}
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

@app.route('/about')
def about():
    if not session.get('logged_in'):
        return render_template('about.html', page='about')
    else:
        return render_template('about.html', page='about', user_id=session['user_id'])

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

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    elif request.method == 'POST':
        email = request.form['email']
        if dbOps.get_user_by_email(email) is None:
            flash('The email you entered is not associated with any account. Please verify the email address.', 'danger')
            return redirect(url_for('forgot_password'))
        else:
            token = Token.generate_confirmation_token(email)
            recover_password_url = url_for('reset_password', token=token, _external=True)
            html = render_template('reset_password.html', recover_password_url=recover_password_url)
            subject = "BookSwap - Password Recovery"
            mail_manager.send_email(email, subject, html)
            flash("An email has been sent to your account, please follow the link to reset your password.", 'success')
            return redirect(url_for('index'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        token = request.args.get('token')
        return render_template('update_password.html', token=token)
    elif request.method == 'POST':
        token = request.form['token']
        email = Token.confirm_token(token)
        new_password = request.form['password']
        errors = []
        errors.append(validate_password(new_password))
        flattened_errors_list = [error for errorSublist in errors for error in errorSublist]
        if(len(flattened_errors_list) == 0):
            user = dbOps.get_user_by_email(email)
            dbOps.edit_user_account(user.user_id, None, encrypt(new_password))
            flash("Successfully updated password", 'Success')
            return render_template('index.html')
        else:
            formatted_error = '. '.join(str(error) for error in flattened_errors_list)
            flash(formatted_error)
            return render_template('update_password.html', token=token)


@app.route('/contact_seller', methods=['POST'])
def contact_seller():
    message = request.form['contact_message']
    email = request.form['contact_recipient'] # Email of person that posted the textbook
    sender_email = request.form['contact_email'] # Email of person that is interested in textbook
    post_id = request.form['post_id']
    user_id = session['user_id']
    book_for_sale = dbOps.get_post(post_id)
    dbOps.send_contact_seller_email(email, sender_email, mail_manager, message, book_for_sale.textbook_title)
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


@app.route('/edit_account/<string:user_id>', methods=['GET', 'POST'])
def edit_account(user_id):
    form = EditAccountForm(request.form)
    if not session.get('logged_in'):
        return "You are not logged in"
    user = dbOps.get_user_by_ID(user_id)
    if not user:
        return "No user account associated with that user"
    if request.method == 'GET':
        return render_template("edit_account_page.html", user_id=user_id, form=form)
    if request.method == 'POST' and form.validate():
        errors = []
        new_email = form.email.data
        new_pword = form.password.data
        if (not new_email) and (not new_pword):
            errors += ['Please enter a new email or password']
        errors += validate_password(new_pword) + validate_email(new_email)
        if dbOps.user_exists(new_email):
            flash("Account already exists for this email")
            return render_template("edit_account_page.html", user_id=user_id, form=form)
        if len(errors) is not 0:
            if errors[0] !='field is required':
                flash(errors[0])
                return render_template("edit_account_page.html", user_id=user_id, form=form)
        if new_email:
            dbOps.send_verification_email(new_email, mail_manager)
            flash("you will receive a confirmation email with an activation URL, to prove that the new email address belongs to you")
            dbOps.edit_user_account(user_id, new_email, encrypt(new_pword))
            return redirect(url_for('index'))
        dbOps.edit_user_account(user_id, new_email, encrypt(new_pword))
        flash("Account successfully updated")
        return redirect(url_for('show_user_page', user_id=user_id))
    else:
        flash("Please fix any errors")
        return render_template("edit_account_page.html", user_id=user_id, form=form)


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
        email = request.values['contact_seller_email']
        if email and validate_email(email) is None:
            flash("Email address is not valid")
            return render_template("create_post_page.html")
        if not title:
            flash("You need to submit a title for the book")
            return render_template("create_post_page.html")

        newpost = dbOps.insert_post(title, user_id, author, email)
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
            pagination = Pagination(page=page, total=len(posts), search=False, record_name='posts', per_page=per_page, css_framework='foundation')
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
            posts_json = json.dumps(posts_dictionary)
            return posts_json
        else:
            posts_json = json.dumps({'posts_data': []})
            return posts_json


@app.route('/post/<string:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    if not session.get('logged_in'):
        return 'You are not logged in'
    if request.method == 'GET':
        post = dbOps.get_post(post_id=post_id)
        if post:
            return render_template("post_page.html", post=post, user_id=session['user_id'])
        else:
            return "The post you are trying to access does not exist"

    if request.method == 'POST':
        creator = dbOps.get_post(post_id=post_id).creator
        if request.form['submit'] == 'Delete this post':
            dbOps.remove_post(post_id)
            flash("Post deleted successfully")
            return redirect(url_for("show_user_page", user_id=creator.user_id))
        elif request.form['submit'] == 'Edit this post':
            return redirect(url_for("edit_post", post_id=post_id))

    else:
        return 'No other options implemented yet'

@app.route('/edit_post/<string:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = dbOps.get_post(post_id=post_id)
    form = EditPostForm(request.form, obj=post)
    creator = post.creator
    user_id = session['user_id']
    if not session.get('logged_in'):
        return "You are not logged in"
    if not creator.user_id==user_id:
        return "You do not have permission to edit this post"
    post = dbOps.get_post(post_id)
    if not post:
        return "This post does not exist"
    if request.method == 'GET':
        return render_template("edit_post_page.html", post_id=post_id, form=form)
    if request.method == 'POST' and form.validate():
        new_title = form.textbook_title.data
        new_author = form.textbook_author.data
        if (not new_title) or (not new_author):
            errors = ['Please enter a title or author']
            flash(errors[0])
            return render_template("edit_post_page.html", post_id=post_id, form=form)
        dbOps.update_existing_post(post_id, new_title, new_author)
        flash('Post has been updated')
        return redirect(url_for('show_user_page', user_id=creator.user_id))



@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.pop('logged_in', None)
        return render_template("index.html")

app.secret_key = 'FOX98PPPCATCHER09FREEFLIGHT'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
