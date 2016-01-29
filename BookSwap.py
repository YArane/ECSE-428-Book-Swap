from flask import Flask, request, render_template, redirect, url_for
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
def hello_world():
    return 'Hello Slack!'

@app.route('/create_account', methods = ['POST'])
def create_account():
    error = []
    if request.method == 'POST':
        error = validate_password(request.form['password'])
        error.append(validate_email(request.form['email']))

    if not error:
        # TODO: encrypt credentials
        # TODO: write encrypted-credentials to database
        return render_template('homepage.html')

    return render_template('create_account.html', error=error)

@app.route('/login', methods = ['POST'])
def login():
    error = []
    if request.method == 'POST':
        pass
        #error = validate_credentials(request.form['email'], request.form['password'])

    if not error:
        return render_template('homepage.html')

    return render_template('login.html', error=error)

@app.route('/user/<int:user_id>/', methods=['GET', 'POST'])
def show_user_page(user_id):
    if request.method == 'GET':
        return render_template('user_page.html', user_id=user_id)
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

