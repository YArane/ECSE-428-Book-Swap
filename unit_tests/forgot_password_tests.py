import mongoengine, unittest
from database.operations import DBOperations
import BookSwap
from encryption.encryption import encrypt

DB = DBOperations()

email_success = "An email has been sent to your account, please follow the link to reset your password."
email_failure = "The email you entered is not associated with any account. Please verify the email address."


class ForgotPasswordTestCase(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost', port=57589)
        DB.delete_users()
        BookSwap.app.config.update(
            MONGODB_SETTINGS={'DB': 'testDB', 'alias':'default', 'port':57589}
        )
        BookSwap.app.config['TESTING'] = True
        BookSwap.app.config['SECRET_KEY'] = '112SOMESECRETKEY987'
        self.app = BookSwap.app.test_client()
        self.create_test_account()

    def tearDown(self):
        DB.delete_users()

    def create_test_account(self):
        DB.insert_user("test@test.com", encrypt("Somepass1234"))
        DB.activate_user("test@test.com")

    def test_forgot_password_get(self):
        with self.app as c:
            resp = c.get('/forgot_password', follow_redirects=True)
            assert resp.status_code is 200
            page_data = resp.get_data()
            assert '<h1>Recover Your Password</h1>' in page_data

    def test_forgot_password_post(self):
        with self.app as c:
            resp = c.post('/forgot_password', data=dict(
                email="test@test.com",
            ), follow_redirects=True)
            assert resp.status_code is 200
            page_data = resp.get_data()
            assert email_success in page_data

    def test_forgot_password_invalid_email(self):
        with self.app as c:
            resp = c.post('/forgot_password', data=dict(
                email="notarealemail@test.com",
            ), follow_redirects=True)
            assert resp.status_code is 200
            page_data = resp.get_data()
            assert email_failure in page_data


if __name__ == '__main__':
    unittest.main()
