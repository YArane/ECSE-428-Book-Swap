from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from account_management.email import MailManager
from config import BaseConfig

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

print app.config

from account_management.create_account import *
from database.models import db
db.init_app(app)

# initialize email object
mail = Mail(app)

mail_manager = MailManager(mail, app)

msg = Message(
        "Hey There!",
        sender=BaseConfig.MAIL_USERNAME,
        recipients=['danielmacario5@gmail.com']
    )
msg.body = "PLEASE VERIFY YOUR SHIT!"

with app.app_context():
    mail.send(msg)


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

@app.route('/create_account', methods = ['POST'])
def create_account():
    error = []
    password = request.form['password']
    email = request.form['email']
    if request.method == 'POST':
        error = validate_password(password)
        error.append(validate_email(email))

    if not error[0]:
        if dbOperations.user_exists(email):
            flash("Account already exists for this email")
            return render_template('signup.html', error=error)
        else:
            dbOperations.insert_user(email, password)
            dbOperations.send_verification_email(email, mail_manager)
            return render_template('index.html')
    else:
        flash("Please enter a valid email and password")
        print error
        return render_template('signup.html')

        # TODO: encrypt credentials
        # TODO: write encrypted-credentials to database

@app.route('/login', methods = ['POST'])
def login():
    error = []
    if request.method == 'POST':
        is_valid = dbOperations.validate_login_credentials(request.form['email'], request.form['password'])
        user = dbOperations.get_user_by_email(request.form['email'])
        if is_valid:
            return redirect(url_for('show_user_page', user_id=user.user_id))
        else:
            flash("invalid login credentials")
            return render_template("index.html")


@app.route('/user/<string:user_id>/', methods=['GET', 'POST'])
def show_user_page(user_id):
    if request.method == 'GET':
        user = dbOperations.get_user_by_ID(user_id)
        if user: # TODO: check that user is authenticated before showing user page
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
        newpost = dbOperations.insert_post(title, user_id, author) #TODO: automatically get current user id
        return redirect(url_for('show_post', post_id=newpost.post_id))


@app.route('/post/<string:post_id>/', methods=['GET', 'POST'])
def show_post(post_id):
    if request.method == 'GET':
        post = dbOperations.get_post(post_id=post_id)
        if post:
            return "Post page for post of textbook " + post.textbook_title + " from user with ID " + str(post.creator.user_id)
        else:
            return "No post on Sundays"

    if request.method == 'POST':
        if request.values['delete'] == 'true':
            dbOperations.remove_post(post_id)
            return "Deleted post with ID %s".format(post_id)
        else:
            return 'No other options implemented yet'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)

