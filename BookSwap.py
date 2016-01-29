from flask import Flask, request, render_template
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

@app.route('/create_acount', methods = ['POST'])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
