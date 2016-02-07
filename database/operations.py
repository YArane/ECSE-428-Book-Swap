import uuid
from account_management.token import Token
from account_management.create_account import validate_email
from flask import flash, redirect, render_template, url_for
from models import Post, User
'''
This class is the layer used to interact with the database. The functions defined here
will let you add, remove, update records on the database. Just create an instance of this
class and use it communicate with the DB. Feel free to add more operations!
'''
tokenizer = Token()


class DBOperations():

    def user_exists(self, email):
        exists = True
        try:
            User.objects.get(email=email)
        except:
            exists = False

        return exists

    def send_verification_email(self, email, mail_manager):
        token = tokenizer.generate_confirmation_token(email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('confirmation.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        mail_manager.send_email(email, subject, html)
        flash('A confirmation email has been sent via email.', 'success')

#       send the email here

    def validate_login_credentials(self, email, password):
        is_valid = True
        try:
            User.objects.get(email=email, password=password)
        except:
            is_valid = False

        return is_valid

    def insert_user(self, email, password):
        user_id = uuid.uuid4()
        new_user = User(email=email, password=password, activated=False, user_id=user_id)
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

    def is_user_account_activated(self, email):
        user_document = User.objects.get(email=email)
        return user_document.activated

    def get_user_by_email(self, email):
        try:
            return User.objects.get(email=email)
        except:
            return None

    def get_user_by_ID(self, user_id):
        try:
            return User.objects.get(user_id=user_id)
        except:
            return None

    def insert_post(self, textbook_title, creator_id, textbook_author=None):
        post_id = uuid.uuid4()
        creator = User.objects.get(user_id=creator_id)
        if textbook_author:
            new_post = Post(textbook_title=textbook_title, creator=creator, textbook_author=textbook_author, post_id=post_id)
        else:
            new_post = Post(textbook_title=textbook_title, creator=creator, post_id=post_id)
        new_post.save()
        return new_post

    def get_post(self, post_id):
        try:
            return Post.objects.get(post_id=post_id)
        except Exception as e:
            return None

    def confirm_email(self, token):
        email = None
        try:
            email = tokenizer.confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('index'))
        user = User.objects.get(email=email)
        if user.activated:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.activated = True
            self.activate_user(email)
            flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('index'))

    # This is just for testing sake
    def delete_users(self):
        return User.objects.delete()

    def remove_post(self, post_id):
        try:
            Post.objects.get(post_id=post_id).delete()
        except:
            return "Couldn't find post with ID " + str(post_id)
        return "Successfully deleted post with ID " + str(post_id)
