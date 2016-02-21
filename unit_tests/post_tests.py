import mongoengine, unittest
from database.operations import DBOperations
DB = DBOperations()


class PostsTestCase(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost')
        DB.delete_posts()

    def create_a_post(self):
        creator = DB.get_user_by_email("test@test.com")
        post = DB.insert_post("bookname", creator.user_id, "authorname")
        return post

    def test_no_posts_in_DB(self):
        posts = DB.get_all_posts()
        self.assertFalse(posts)

    def test_one_post_in_DB(self):
        self.create_a_post()
        posts = DB.get_all_posts()
        self.assertEquals(posts[0].textbook_title, "bookname")

if __name__ == '__main__':
    unittest.main()