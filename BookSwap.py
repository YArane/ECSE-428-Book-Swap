from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Slack!'


@app.create_account('/create_acount', methods = ['POST'])
def create_account():



if __name__ == '__main__':
    app.run()
