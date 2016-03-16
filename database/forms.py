from wtforms import Form, TextField, PasswordField


class EditAccountForm(Form):
    email = TextField('New email address')
    password = PasswordField('New password')
