import uuid
from models import User, Post
from account_management.create_account import validate_password, validate_email

'''
This class is the layer used to interact with the database. The functions defined here
will let you add, remove, update records on the database. Just create an instance of this
class and use it communicate with the DB. Feel free to add more operations!
'''

class DBOperations():

    def __init__(self):
        pass

    def user_exists(self, email):
        exists = True
        try:
            User.objects.get(email=email)
        except:
            exists = False

        return exists

    def validate_login_credentials(self, email, password):
        is_valid = True
        try:
            User.objects.get(email=email, password=password)
        except:
            is_valid = False

        return is_valid

    def insert_user(self, email, password):
        new_user = User(email=email, password=password, activated=False)
        new_user.save()


    def activate_user(self, email):
        valid_email = len(validate_email(email)) == 0
        if (valid_email):
            try:
                user_document = User.objects.get(email=email)
                user_document.activated = True
                user_document.save()
                return True
            except:
                print "Error occurred trying to activate user for email = " + email
        return False

    def insert_post(self, textbook_title, creator_email, textbook_author=None):
        post_id = uuid.uuid4()
        creator = User.objects.get(email=creator_email)
        if textbook_author:
            new_post = Post(textbook_title=textbook_title, creator=creator_email, textbook_author=textbook_author, post_id=post_id)
        else:
            new_post = Post(textbook_title=textbook_title, creator=creator_email, post_id=post_id)
        new_post.save()
        return new_post

    def get_post(self, post_id):
        try:
            return Post.objects.get(post_id=post_id)
        except Exception as e:
            return e

    # This is just for testing sake
    def delete_users(self):
        return User.objects.delete()

    def remove_post(self, post_id):
        try:
            Post.objects.get(post_id=post_id).delete()
        except:
            return "Couldn't find post with ID " + str(post_id)
        return "Successfully deleted post with ID " + str(post_id)


