import mongoengine, unittest
from database.operations import DBOperations
from database.models import Post
DB = DBOperations()


class InsertPostTestCase(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost')
        DB.delete_users()
        DB.insert_user("test@test.com", password="Somepass1234")

    def create_a_post(self):
        creator = DB.get_user_by_email("test@test.com")
        post = DB.insert_post("bookname", creator.user_id, "authorname")
        return post

    def test_valid_post_with_user(self):
        post = self.create_a_post()
        self.assertEqual(Post.objects.get(post_id=post.post_id), post)

    def test_valid_post_without_author(self):
        post = self.create_a_post()
        self.assertEqual(Post.objects.get(post_id=post.post_id), post)

    def test_remove_post(self):
        post = self.create_a_post()
        DB.remove_post(post.post_id)
        self.assertNotIn(post, Post.objects.all())


if __name__ == '__main__':
    unittest.main()
