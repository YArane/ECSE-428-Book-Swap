from flask import Flask, request, render_template, redirect, url_for, flash
from account_management.create_account import *
from database.operations import DBOperations

app = Flask(__name__)

app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'bookswap_development'}
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'flask+mongoengine=<3'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

from database.models import db
db.init_app(app)

# Use this object to communicate interact with the DB. See operations.py
# to understand what operations are defined
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

    if not error:
        if dbOperations.user_exists(email):
            flash("account already exists for this email")
            return render_template('signup.html', error=error)
        else:
            dbOperations.insert_user(email, password)
            return render_template('user_page.html')
    else:
        flash("please enter a valid email and password")
        return render_template('signup.html')

        # TODO: encrypt credentials
        # TODO: write encrypted-credentials to database

@app.route('/login', methods = ['POST'])
def login():
    error = []
    if request.method == 'POST':
        is_valid = dbOperations.validate_login_credentials(request.form['email'], request.form['password'])

        if is_valid:
            return render_template('user_page.html')
        else:
            flash("invalid login credentials")
            return render_template("index.html")


@app.route('/user/<int:user_id>/', methods=['GET', 'POST'])
def show_user_page(user_id):
    if request.method == 'GET':
        return render_template('user_page.html', user_id=user_id) #TODO: what is user_id?
    if request.method == 'POST':
        return redirect(url_for('create_post'))


@app.route('/create_post/', methods=['GET', 'POST'])
def create_post():
    return "Create post page"

@app.route('/post/<int:post_id>/', methods=['GET', 'POST'])
def show_post(post_id):
    if request.method == 'GET':
        #this is just a placeholder message, obviously it should check the database for the post and get data from there
        return 'This is the post page of post #%d' % post_id
    if request.method == 'POST':
        if request.values['delete'] == 'true':
            return 'Post would hypothetically get deleted'
        else:
            return 'No other options implemented yet'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)

