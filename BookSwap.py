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
        return render_template('homepage.html')

    return render_template('create_account.html', error=error)

if __name__ == '__main__':
    app.run()
