import re

rgx_password_requirements = [r'(.*[a-z])', \
                         r'(.*[A-Z])', \
                         r'(.*[0-9])', \
                         r'(^\w{8,}$)', \
                         r'(^\w{,30}$)']
password_requirements = ['lowercase required', \
                         'uppercase required', \
                         'number required', \
                         'min length = 8', \
                         'max length = 30']

""" Validates user input password using regex
to find rules that are not obeyed

    password: input string
    return: list of rules which failed
"""
def validate_password(password):
    # check for string type
    if not password:
        return ['field is required']
    if not isinstance(password, basestring):
        return ['alphanumeric characters only']
    if not password.isalnum():
        return ['alphanumeric characters only']

    # check regular expressions
    failed_rules = []
    for rgx, requirement in zip(rgx_password_requirements, password_requirements):
        result = re.match(rgx, password)
        if not result:
           failed_rules.append(requirement)

    return failed_rules

