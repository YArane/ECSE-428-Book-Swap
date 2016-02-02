import unittest
import mongoengine
from database.operations import DBOperations
from database.models import Post
DB = DBOperations()

class InsertPostTestCase(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost')
        DB.delete_users()
        DB.insert_user("test@test.com", "1234")

    def test_valid_post_with_user(self):
        post = DB.insert_post("bookname", "test@test.com", "authorname")
        self.assertEqual(Post.objects.get(post_id=post.post_id), post)

    def test_valid_post_without_author(self):
        post = DB.insert_post("bookname", "test@test.com")
        self.assertEqual(Post.objects.get(post_id=post.post_id), post)

    def test_remove_post(self):
        post = DB.insert_post("bookname", "test@test.com")
        DB.remove_post(post.post_id)
        self.assertNotIn(post, Post.objects.all())


if __name__ == '__main__':
    unittest.main()
