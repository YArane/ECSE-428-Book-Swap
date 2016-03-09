import mongoengine, unittest
from database.operations import DBOperations
from database.models import Post
import BookSwap
import tempfile
import os
import flask
from flask import session, redirect, url_for
from database.models import db

DB = DBOperations()


class BookSwapTestCase(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost', port=57589)
        DB.delete_users()
        BookSwap.app.config.update(
            MONGODB_SETTINGS={'DB': 'testDB', 'alias':'default', 'port':57589}
        )
        BookSwap.app.config['TESTING'] = True
        self.app = BookSwap.app.test_client()
        self.create_test_account()

    def tearDown(self):
        DB.delete_users()

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def create_test_account(self):
        DB.insert_user("test@test.com", password="Somepass1234")
        DB.activate_user("test@test.com")

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login(self):
        self.login("test@test.com", "Somepass1234")
        with self.app as c:
            c.get('/')
            assert flask.session['logged_in']
        self.logout()

if __name__ == '__main__':
        unittest.main()
