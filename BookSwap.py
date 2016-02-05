from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail
from account_management.email import MailManager
from account_management.create_account import validate_email, validate_password

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


# Use this object to communicate interact with the DB. See operations.py
# to understand what operations are defined
from database.operations import DBOperations
dbOperations = DBOperations()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page='index')


@app.route('/signup')
def signup():
    return render_template('signup.html', page='signup')


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
        if dbOperations.user_exists(email):
            flash("Account already exists for this email")
            return render_template('signup.html', error=errors)
        else:
            dbOperations.insert_user(email, password)
            dbOperations.send_verification_email(email, mail_manager)
            return render_template('index.html')
    else:
        print errors
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
        is_valid = dbOperations.validate_login_credentials(email, request.form['password'])
        user = dbOperations.get_user_by_email(email)
        if is_valid:
            if dbOperations.is_user_account_activated(email):
                return redirect(url_for('show_user_page', user_id=user.user_id))
            else:
                flash("Your account has not been activated yet. Please follow the URL in your email")
                return render_template("index.html")
        else:
            flash("invalid login credentials")
            return render_template("index.html")


@app.route('/user/<string:user_id>/', methods=['GET', 'POST'])
def show_user_page(user_id):
    if request.method == 'GET':
        user = dbOperations.get_user_by_ID(user_id)
        if user:  # TODO: check that user is authenticated before showing user page
            return render_template('user_page.html', user_id=user_id)
        else:
            return "No user account associated with that user"

    if request.method == 'POST':
        return redirect(url_for('create_post', user_id=user_id))


@app.route('/create_post/', methods=['GET', 'POST'])
def create_post():
    user_id = request.values['user_id']
    if request.method == 'GET':
        return render_template("create_post_page.html")
    else:
        title = request.values['textbook_title']
        author = request.values['textbook_author']
        newpost = dbOperations.insert_post(title, user_id, author)
        return redirect(url_for('show_post', post_id=newpost.post_id))


@app.route('/post/<string:post_id>/', methods=['GET', 'POST'])
def show_post(post_id):
    if request.method == 'GET':
        post = dbOperations.get_post(post_id=post_id)
        if post:
            return render_template("post_page.html", user=post.creator.email, title=post.textbook_title)
        else:
            return "No post on Sundays"

    if request.method == 'POST':
        dbOperations.remove_post(post_id)
        return "Post deleted successfully"
    else:
        return 'No other options implemented yet'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
