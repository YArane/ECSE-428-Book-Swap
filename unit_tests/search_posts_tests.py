import mongoengine, unittest
from database.operations import DBOperations
DB = DBOperations()


class SearchPostsTest(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('testDB', host='localhost')
        DB.delete_users()
        DB.insert_user("test@test.com", password="Somepass1234")

    def create_posts(self):
        creator = DB.get_user_by_email("test@test.com")
        search_term = "booktitle"
        post = [DB.insert_post(search_term, creator.user_id, "authorname"), DB.insert_post(DB.insert_post(search_term+' extra'))]
        DB.insert_post("textbook title", creator.user_id, "name of author")
        search = {'post': post, 'search_term': search_term}
        return search

    def test_valid_search_posts_existing_title(self):
        search = self.create_posts()
        search_post = DB.search(search['search_term'])
        self.assertEqual(search_post['post'], search_post)

    def search_posts_nonexisting_title(self):
        search_post = DB.search('nil')
        self.assertIsNone(search_post)

    def tearDown(self):
        DB.delete_posts()
        DB.delete_users()
        mongoengine.disconnect('testDB', host='localhost')

if __name__ == '__main__':
    unittest.main()
