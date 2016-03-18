import mongoengine
import BookSwap
from flask import Flask, session, url_for
from flask.ext.testing import TestCase
from database.operations import DBOperations
from encryption.encryption import encrypt
DB = DBOperations()


class EditAccountTestCase(TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost', port=57589)
        DB.delete_users()
        BookSwap.app.config.update(
            MONGODB_SETTINGS={'DB': 'testDB', 'alias':'default', 'port':57589}
        )
        BookSwap.app.config['TESTING'] = True
        BookSwap.app.config['SECRET_KEY'] = '112SOMESECRETKEY987'
        self.app = BookSwap.app.test_client()

        def tearDown(self):
            DB.delete_users()

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def login(self):
        return self.app.post('/login', data=dict(
            email="test@test.com",
            password="Somepass1234"
        ), follow_redirects=True)

    def create_test_account(self):
        DB.insert_user("test@test.com", encrypt("Somepass1234"))
        DB.activate_user("test@test.com")
        return DB.get_user_by_email("test@test.com")

    def test_edit_successfully(self):
        user = self.create_test_account()
        self.login()
        rv = self.app.post('/edit_account/{0}'.format(user.user_id), data=dict(
            email="",
            password="Somepass123"
        ), follow_redirects=True)
        self.assertEqual(str(user.password), encrypt("Somepass1234"))
