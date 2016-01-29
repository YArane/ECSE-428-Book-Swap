from models import User
from account_management.create_account import validate_password_requirement

class DBOperations():

    def __init__(self):
        pass

    def insert_user(self, email, password):
        #TODO: add email validation
        if (validate_password_requirement(password)):
            new_user = User(email=email,
                            password=password,
                            activated=False)
            new_user.save()
            return True
        return False