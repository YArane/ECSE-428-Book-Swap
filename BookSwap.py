from flask import Flask, Markup, request, render_template, redirect, url_for, flash
from flask_mail import Mail
from account_management.email import MailManager
from account_management.create_account import validate_email, validate_password
from encryption.encryption import encrypt

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
    MONGODB_SETTINGS = {'DB': 'bookswap_development', 'alias':'default'}
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

@app.route('/confirm')
def confirm_email():
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
        #print error
        return render_template('signup.html')

        # TODO: encrypt credentials
        # TODO: write encrypted-credentials to database


@app.route('/login', methods=['POST'])
def login():
    error = []
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
        user = dbOps.get_user_by_ID(user_id)
        posts = dbOps.get_posts_by_user(user_id)
        if user:  # TODO: check that user is authenticated before showing user page
            post_titles = [str(p.textbook_title) for p in posts]
            return render_template('user_page.html', user_id=user_id, posts=Markup(post_titles))
        else:
            return "No user account associated with that user"

    if request.method == 'POST':
        return redirect(url_for('create_post', user_id=user_id))


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    user_id = request.values['user_id']
    if request.method == 'GET':
        return render_template("create_post_page.html")
    else:
        title = request.values['textbook_title']
        author = request.values['textbook_author']
        newpost = dbOps.insert_post(title, user_id, author)
        return redirect(url_for('show_post', post_id=newpost.post_id))


@app.route('/post/<string:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    if request.method == 'GET':
        post = dbOps.get_post(post_id=post_id)
        if post:
            return render_template("post_page.html", user=post.creator.email, title=post.textbook_title)
        else:
            return "No post on Sundays"

    if request.method == 'POST':
        dbOps.remove_post(post_id)
        return "Post deleted successfully"
    else:
        return 'No other options implemented yet'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
