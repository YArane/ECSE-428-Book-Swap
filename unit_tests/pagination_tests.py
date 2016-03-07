import unittest
from BookSwap import get_page_items
import flask

app = flask.Flask(__name__)

class PaginationTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_page_set_to_1_if_unspecified(self):
        with app.test_request_context():
            posts_per_page = 20
            page, per_page, offset = get_page_items(posts_per_page)
            self.assertEqual(page, 1)

    def test_page_set_to_value_sent_in_request(self):
        with app.test_request_context('/?page=4'):
            posts_per_page = 20
            page, per_page, offset = get_page_items(posts_per_page)
            self.assertEqual(page, 4)

    def test_correct_posts_per_page_returned(self):
        with app.test_request_context('/?page=16'):
            posts_per_page = 20
            page, per_page, offset = get_page_items(posts_per_page)
            self.assertEqual(per_page, posts_per_page)

    def test_offset_calculated_correctly(self):
        with app.test_request_context('/?page=13'):
            posts_per_page = 20
            page, per_page, offset = get_page_items(posts_per_page)
            self.assertEqual(offset, 240)


if __name__ == '__main__':
    unittest.main()

