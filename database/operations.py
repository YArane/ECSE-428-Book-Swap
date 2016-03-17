import uuid
from account_management.token import Token
from account_management.create_account import validate_email
from flask import flash, redirect, render_template, url_for
from models import Post, User
from flask.ext.mongoengine import MongoEngine

'''
This class is the layer used to interact with the database. The functions defined here
will let you add, remove, update records on the database. Just create an instance of this
class and use it communicate with the DB. Feel free to add more operations!
'''
db = MongoEngine()

class DBOperations():

    @staticmethod
    def user_exists(email):
        exists = True
        try:
            User.objects.get(email=email)
        except:
            exists = False

        return exists

    @staticmethod
    def send_verification_email(email, mail_manager):
        token = Token.generate_confirmation_token(email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('confirmation.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        mail_manager.send_email(email, subject, html)
        flash('A confirmation email has been sent via email.', 'success')

#       send the email here

    @staticmethod
    def send_contact_seller_email(email, sender_email, mail_manager, message):
        token = Token.generate_confirmation_token(email)
        confirm_url = url_for('contact_seller', token=token, _external=True)
        if message == '':
            message = "Message from " + sender_email + ":\n\n" + "Hello! I am interested in buying your textbook!"
        html = render_template('contact_seller_confirmation.html', message=message, sender_email=sender_email)
        subject = "Interest in your textbook"
        mail_manager.send_email(email, subject, html)
        flash('Your message has been sent!', 'success')

    @staticmethod
    def validate_login_credentials(email, password):
        is_valid = True
        try:
            User.objects.get(email=email, password=password)
        except:
            is_valid = False

        return is_valid

    @staticmethod
    def insert_user(email, password):
        user_id = uuid.uuid4()
        new_user = User(email=email, password=password, activated=False, user_id=user_id)
        new_user.save()

    @staticmethod
    def activate_user(email):
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

    @staticmethod
    def edit_user_account(user_id, email, password):
        user = User.objects.get(user_id=user_id)
        if email:
            user.activated = False
            user.email = email
        if password:
            user.password = password
        user.save()

    @staticmethod
    def is_user_account_activated(email):
        user_document = User.objects.get(email=email)
        return user_document.activated

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return None

    @staticmethod
    def get_user_by_ID(user_id):
        try:
            return User.objects.get(user_id=user_id)
        except:
            return None

    @staticmethod
    def insert_post(textbook_title, creator_id, textbook_author=None):
        post_id = uuid.uuid4()
        creator = User.objects.get(user_id=creator_id)
        if textbook_author:
            new_post = Post(textbook_title=textbook_title, creator=creator, textbook_author=textbook_author, post_id=post_id)
        else:
            new_post = Post(textbook_title=textbook_title, creator=creator, post_id=post_id)
        new_post.save()
        return new_post

    @staticmethod
    def update_existing_post(post_id, new_title, new_author):
        # Pass in the id of the post you want to modify as a string
        # A new title and a new author (both also strings)
        # This operation will store the changes in the database
        try:
            post = Post.objects.get(post_id=post_id)
            post.textbook_author = new_author
            post.textbook_title = new_title
            post.save()
        except Exception as e:
            print "Failed to update post"


    @staticmethod
    def get_post(post_id):
        try:
            return Post.objects.get(post_id=post_id)
        except Exception as e:
            return None

    @staticmethod
    def get_all_posts():
        try:
            return Post.objects.all()
        except Exception as e:
            return None

    @staticmethod
    def get_posts_by_user(user_id):
        retval = []
        for post in Post.objects.all():
            if str(post.creator.user_id) == str(user_id):
                retval.append(post)
        return retval

    @staticmethod
    def get_most_recent_posts_by_user(user):
        # You need to pass the User object from the DB. Not the ID.
        posts_by_user = Post.objects(creator=user.id).order_by('-date_posted') # the '-' sign is for decreasing
        return posts_by_user

    @staticmethod
    def get_oldest_first_posts_by_user(user):
        # You need to pass the User object from the DB. Not the ID.
        posts_by_user = Post.objects(creator=user.id).order_by('+date_posted') # the '+' sign is for decreasing
        return posts_by_user

    @staticmethod
    def search(query):
        Post.ensure_index([('textbook_title', 'text'),])
        posts = Post.objects.search_text(query).order_by('$text_score')
        return posts

    @staticmethod
    def confirm_email(token):
        email = None
        try:
            email = Token.confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('index'))
        try:
            user = User.objects.get(email=email)
            if user.activated:
                flash('Account already confirmed. Please login.', 'success')
            else:
                user.activated = True
                DBOperations.activate_user(email)
                flash('You have confirmed your account. Thanks!', 'success')
        except:
            flash('The account activation URL specified is not associated to any account', 'danger')
        return redirect(url_for('index'))

    @staticmethod
    def contact_seller_confirm_email(token):
        return redirect(url_for('post_page'))

    # This is just for testing sake
    @staticmethod
    def delete_users():
        return User.objects.delete()

    @staticmethod
    def delete_posts():
        return Post.objects.delete()

    @staticmethod
    def remove_post(post_id):
        try:
            Post.objects.get(post_id=post_id).delete()
        except:
            return "Couldn't find post with ID " + str(post_id)
        return "Successfully deleted post with ID " + str(post_id)
