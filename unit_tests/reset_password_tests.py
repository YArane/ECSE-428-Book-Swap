import mongoengine, unittest
from database.operations import DBOperations
import BookSwap
from encryption.encryption import encrypt, decrypt
from account_management.token import Token

DB = DBOperations()

test_email = "test@test.com"
test_password = "Somepass1234"
new_test_password = "Somepass12345"
new_weak_password = "123"
reset_password_success = "<h1>Update Your Password</h1>"
update_password_success = "Successfully updated password"
email_failure = "The email you entered is not associated with any account. Please verify the email address."
weak_password_message = "Password must be at least 8 alphanumeric characters long"


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
        DB.insert_user(test_email, encrypt(test_password))
        DB.activate_user(test_email)

    def test_reset_password_get(self):
        with self.app as c:
            resp = c.get('/reset-password', data=dict(
                token = Token.generate_confirmation_token(test_email)
            ), follow_redirects=True)
            assert resp.status_code is 200
            page_data = resp.get_data()
            assert reset_password_success in page_data

    def test_reset_password_post(self):
        with self.app as c:
            resp = c.post('/reset-password', data=dict(
                token = Token.generate_confirmation_token(test_email),
                password = new_test_password
            ), follow_redirects=True)
            assert resp.status_code is 200
            page_data = resp.get_data()
            assert update_password_success in page_data

    def test_password_is_updated(self):
        with self.app as c:
            c.post('/reset-password', data=dict(
                token = Token.generate_confirmation_token(test_email),
                password = new_test_password
            ), follow_redirects=True)
            user = DB.get_user_by_email(test_email)
            self.assertEqual(decrypt(user.password), new_test_password)

    def test_weak_password_rejected(self):
        with self.app as c:
            resp = c.post('/reset-password', data=dict(
                token = Token.generate_confirmation_token(test_email),
                password = new_weak_password
            ), follow_redirects=True)

            assert resp.status_code is 200
            page_data = resp.get_data()
            assert weak_password_message in page_data


if __name__ == '__main__':
    unittest.main()
