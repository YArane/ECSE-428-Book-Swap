import unittest
from account_management.create_account import validate_password_requirement

class TestPasswordRequirementMethod(unittest.TestCase):

    def test_lowercase(self):
        self.assertEqual(validate_password_requirement("ABCDEFG123"), ['lowercase required'])
        self.assertEqual(validate_password_requirement("abcdefG123"), [])

    def test_uppercase(self):
        self.assertEqual(validate_password_requirement("abcdefg123"), ['uppercase required'])
        self.assertEqual(validate_password_requirement("ABCDEFg123"), [])

    def test_number(self):
        self.assertEqual(validate_password_requirement("abcdefgHIJ"), ['number required'])
        self.assertEqual(validate_password_requirement("ABCDEFg123"), [])

    def test_min_length(self):
        self.assertEqual(validate_password_requirement("ABC1fgh"), ['min length = 8'])
        self.assertEqual(validate_password_requirement("ABCDg234"), [])

    def test_max_length(self):
        self.assertEqual(validate_password_requirement("abcdefghijklmnopqrstuvwxyzABCDEFG123456789"), ['max length = 30'])
        self.assertEqual(validate_password_requirement("abcdefghijklmnopqrstuvwxyzABC1"), [])

    def test_null(self):
        self.assertEquals(validate_password_requirement(""), ['field is required'])
        self.assertEquals(validate_password_requirement(None), ['field is required'])

    def test_symbols(self):
        self.assertEquals(validate_password_requirement("abc^ABC123"), ['alphanumeric characters only'])
        self.assertEquals(validate_password_requirement("abc~:ABC123"), ['alphanumeric characters only'])

    def test_general(self):
        self.assertEquals(validate_password_requirement("passwor"), ['uppercase required', 'number required', 'min length = 8'])
        self.assertEquals(validate_password_requirement(123), ['alphanumeric characters only'])

if __name__ == '__main__':
    unittest.main()
