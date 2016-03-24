from wtforms import Form, TextField, PasswordField, StringField


class EditAccountForm(Form):
    email = TextField('New email address')
    password = PasswordField('New password')

class EditPostForm(Form):
    textbook_title = TextField('Updated Textbook Title')
    textbook_author = TextField('Updated Textbook Author')
