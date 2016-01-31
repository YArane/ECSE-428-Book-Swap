import unittest
from account_management.create_account import validate_password
from account_management.create_account import validate_email
from account_management.create_account import validate_credentials


class TestPasswordRequirementMethod(unittest.TestCase):

    def test_lowercase(self):
        self.assertEqual(validate_password("ABCDEFG123"), ['lowercase required'])
        self.assertEqual(validate_password("abcdefG123"), [])

    def test_uppercase(self):
        self.assertEqual(validate_password("abcdefg123"), ['uppercase required'])
        self.assertEqual(validate_password("ABCDEFg123"), [])

    def test_number(self):
        self.assertEqual(validate_password("abcdefgHIJ"), ['number required'])
        self.assertEqual(validate_password("ABCDEFg123"), [])

    def test_min_length(self):
        self.assertEqual(validate_password("ABC1fgh"), ['min length = 8'])
        self.assertEqual(validate_password("ABCDg234"), [])

    def test_max_length(self):
        self.assertEqual(validate_password("abcdefghijklmnopqrstuvwxyzABCDEFG123456789"), ['max length = 30'])
        self.assertEqual(validate_password("abcdefghijklmnopqrstuvwxyzABC1"), [])

    def test_null(self):
        self.assertEquals(validate_password(""), ['field is required'])
        self.assertEquals(validate_password(None), ['field is required'])

    def test_symbols(self):
        self.assertEquals(validate_password("abc^ABC123"), ['alphanumeric characters only'])
        self.assertEquals(validate_password("abc~:ABC123"), ['alphanumeric characters only'])

    def test_general(self):
        self.assertEquals(validate_password("passwor"), ['uppercase required', 'number required', 'min length = 8'])
        self.assertEquals(validate_password(123), ['string characters only'])

class TestVaildateEmailMethod(unittest.TestCase):

    def test_syntax(self):
        self.assertEquals(validate_email("yarden.arane@gmail.com"), [])
        self.assertEqual(validate_email('skatie_girl57@.com'), ['invalid syntax'])

    def test_null(self):
        self.assertEquals(validate_email(""), ['field is required'])
        self.assertEquals(validate_email(None), ['field is required'])



class TestValidateCredentials(unittest.TestCase):

    def test_true(self):
        self.assertEquals(validate_credentials("yarden.arane@gmail.com", 'abcDEF123'), True)

    def test_false(self):
        self.assertEquals(validate_credentials("yrden.arane@gmail.com", 'abcDEF123'), False)


if __name__ == '__main__':
    unittest.main()
