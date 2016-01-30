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

    def insert_user(self, email, password):
        #TODO: talk to Yarden about where we should put the validation logic
        # Here or on the routes?

        valid_password = len(validate_password(password)) == 0
        valid_email = len(validate_email(email)) == 0

        if (valid_password and valid_email):
            new_user = User(email=email,
                            password=password,
                            activated=False)
            new_user.save()
            return True
        return False

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

    def insert_post(self, textbook_name, creator_id, textbook_author=None):
        creator = User.objects.get(user_id=creator_id)
        if textbook_author:
            new_post = Post(textbook_name, creator, textbook_author)
        else:
            new_post = Post(textbook_name, creator)
        new_post.save()
