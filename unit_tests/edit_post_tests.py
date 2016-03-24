import mongoengine
import BookSwap
from flask import Flask
from flask.ext.testing import TestCase
from database.operations import DBOperations
from encryption.encryption import encrypt
DB = DBOperations()


class EditPostTestCase(TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost', port=57589)
        DB.delete_users()
        DB.delete_posts()
        BookSwap.app.config.update(
            MONGODB_SETTINGS={'DB': 'testDB', 'alias':'default', 'port':57589}
        )
        BookSwap.app.config['TESTING'] = True
        BookSwap.app.config['SECRET_KEY'] = '112SOMESECRETKEY987'
        self.app = BookSwap.app.test_client()

    def tearDown(self):
        DB.delete_users()
        DB.delete_posts()

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def login(self):
        return self.app.post('/login', data=dict(
            email="test@test.com",
            password="Somepass1234"
        ), follow_redirects=True)

    def create_test_account_and_post(self):
        DB.insert_user("test@test.com", encrypt("Somepass1234"))
        DB.activate_user("test@test.com")
        user = DB.get_user_by_email("test@test.com")
        post = DB.insert_post('test_title', user.user_id, 'test_author', user.email)
        return dict(user=user, post=post)

    def test_edit_posts_db(self):
        params = self.create_test_account_and_post()
        post = params['post']
        new_title = "test_title2"
        new_author = "test_author2"
        DB.update_existing_post(post.post_id, new_title, new_author)
        updated_post = DB.get_post(post.post_id)
        self.assertEqual(new_title, updated_post.textbook_title)
        self.assertEqual(new_author, updated_post.textbook_author)

    def test_edit_successfully(self):
        params = self.create_test_account_and_post()
        post = params['post']
        self.login()
        self.app.post('/edit_post/{0}'.format(post.post_id), data=dict(
            textbook_title="test_title2",
            textbook_author="test_author2"
        ), follow_redirects=True)
        updated_post = DB.get_post(post.post_id)
        self.assertEqual(updated_post.textbook_title, "test_title2")
        self.assertEqual(updated_post.textbook_author, "test_author2")
