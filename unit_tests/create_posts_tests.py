import mongoengine, unittest
from database.operations import DBOperations
from database.models import Post
DB = DBOperations()


class InsertPostTestCase(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost', port=57589)
        DB.delete_users()
        DB.insert_user("test@test.com", password="Somepass1234")

    def create_a_post(self):
        creator = DB.get_user_by_email("test@test.com")
        post = DB.insert_post("bookname", creator.user_id)
        return post

    def create_a_post_with_author(self):
        creator = DB.get_user_by_email("test@test.com")
        post = DB.insert_post("bookname", creator.user_id, "authorname")
        return post

    def create_a_post_with_contact_email(self):
        creator = DB.get_user_by_email("test@test.com")
        post = DB.insert_post("bookname", creator.user_id, "authorname", "test@test.com")
        return post

    def test_valid_post_with_user(self):
        post = self.create_a_post()
        self.assertEqual(Post.objects.get(post_id=post.post_id), post)

    def test_valid_post_with_author(self):
        post = self.create_a_post_with_author()
        self.assertEqual(Post.objects.get(post_id=post.post_id), post)
        self.assertEquals(post.textbook_author, "authorname")

    def test_valid_post_with_contact_email(self):
        post = self.create_a_post_with_contact_email()
        self.assertEqual(Post.objects.get(post_id=post.post_id), post)
        self.assertEquals(post.contact_seller_email, "test@test.com")

    def test_remove_post(self):
        post = self.create_a_post()
        DB.remove_post(post.post_id)
        self.assertNotIn(post, Post.objects.all())


if __name__ == '__main__':
    unittest.main()
