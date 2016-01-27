from flask import Flask

app = Flask(__name__)

app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'testing'}
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'flask+mongoengine=<3'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

from models import db
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello Slack!'

@app.route('/create_acount', methods = ['POST'])
def create_account():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)