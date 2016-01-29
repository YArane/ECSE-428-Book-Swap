import datetime
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):
    email = db.StringField(max_length=30, required=True)
    password = db.StringField(max_length=30, required=True)
    activated = db.BooleanField(default=False)