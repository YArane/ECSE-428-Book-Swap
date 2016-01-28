from flask import Flask
from account_management.create_account import *

app = Flask(__name__)


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
        error = validate_credentials(request.form['email'], request.form['password'])

    if not error:
        return render_template('homepage.html')

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
