from models import User
from account_management.create_account import validate_password, validate_email

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

