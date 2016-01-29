import datetime
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

'''
This file will contain all the models used by the database. You can think of the User
model below as a table with 3 columns: email, password, and a boolean activated.
Eventually we will need models for BookPosts, and many others.
'''

class User(db.Document):
    email = db.StringField(max_length=30, required=True)
    password = db.StringField(max_length=30, required=True)
    activated = db.BooleanField(default=False)