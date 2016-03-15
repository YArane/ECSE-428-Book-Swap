from wtforms import Form, BooleanField, TextField, PasswordField, validators


class EditAccountForm(Form):
    email = TextField('New email address')
    password = PasswordField('New password')
