import mongoengine, unittest
from database.operations import DBOperations
import BookSwap
from encryption.encryption import encrypt

DB = DBOperations()

test_email = "test@test.com"
test_password = "Somepass1234"

contact_seller_success_message = "Your message has been sent!"

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

    def login(self):
        return self.app.post('/login', data=dict(
            email=test_email,
            password=test_password
        ), follow_redirects=True)

    def test_contact_seller_with_message(self):
        with self.app as c:
            self.login()
            resp = c.post('/contact_seller', data=dict(
                contact_message = "Hola! Quiero comprar tu libro.",
                contact_recipient = "someone@test.com",
                contact_email = test_email
            ), follow_redirects=True)
            print resp.status_code
            assert resp.status_code is 200
            page_data = resp.get_data()
            assert contact_seller_success_message in page_data

    def test_contact_seller_without_message(self):
        with self.app as c:
            self.login()
            resp = c.post('/contact_seller', data=dict(
                contact_message = "",
                contact_recipient = "someone@test.com",
                contact_email = test_email
            ), follow_redirects=True)
            assert resp.status_code is 200
            page_data = resp.get_data()
            assert contact_seller_success_message in page_data


if __name__ == '__main__':
    unittest.main()
