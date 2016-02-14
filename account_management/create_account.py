import re

rgx_password_requirements = [r'(.*[a-z])', \
                         r'(.*[A-Z])', \
                         r'(.*[0-9])', \
                         r'(^\w{8,}$)', \
                         r'(^\w{,30}$)']
password_requirements = ['Lowercase character required', \
                         'Uppercase character required', \
                         'Number required', \
                         'Password must be at least 8 alphanumeric characters long', \
                         'Password must be at most 30 alphanumeric characters long']

""" Validates user input password using regex
to find rules that are not obeyed

    password: input string
    return: list of rules which have failed
"""
def validate_password(password):
    valid = verify_input(password)
    if(valid == 1):
        pass
    else:
       return valid

    if not password.isalnum():
        return ['alphanumeric characters only']

    # check regular expressions
    failed_rules = []
    for rgx, requirement in zip(rgx_password_requirements, password_requirements):
        result = re.match(rgx, password)
        if not result:
           failed_rules.append(requirement)


    return failed_rules


""" Validates user input email address using regex
to find rules that are not obeyed

    password: input string
    return: list of rules which have failed
"""
def validate_email(email):
    valid = verify_input(email)
    if(valid == 1):
        pass
    else:
       return valid

    # check syntax
    valid_syntax = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if not valid_syntax:
        return ['The email address submitted is invalid']
    return []

""" Validates user input email and password
against database entries

    email: input email
    password: input password
    return: True, False
"""
def validate_credentials(email, password):
    valid = verify_input(email) * verify_input(password)
    if(valid == 1):
        pass
    else:
       return valid

    e = 'yarden.arane@gmail.com'
    p = 'abcDEF123'

    if email == e and password == p:
        return True

    return False


""" private method.
checks properties of input string for parsing
"""
def verify_input(string):
    # check for string type
    if not string:
        return ['field is required']
    if not isinstance(string, basestring):
        return ['string characters only']
    return 1
