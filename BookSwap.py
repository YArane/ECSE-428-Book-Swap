from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Slack!'


@app.route('/create_acount', methods = ['POST'])
def create_account():
    pass


if __name__ == '__main__':
    app.run()
