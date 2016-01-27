import re

rgx_password_requirements = [r'(.a*[a-z])', \
                         r'(.*[A-Z])', \
                         r'(.*[0-9])', \
                         r'(.[a-zA-Z0-9]{8,30})']
password_requirements = ['lowercase required', \
                         'uppercase required', \
                         'number required', \
                         'min len = 8, max len = 30']

""" Validates user input password using regex
to find rules that are not obeyed

    password: input string
    return: list of rules which failed
"""
def validate_password_requirement(password):
    failed_rules = []
    for rgx, requirement in zip(rgx_password_requirements, password_requirements):
        result = re.match(rgx, password)
        if not result:
           failed_rules.append(requirement)

    return failed_rules

password = 'YSNAPREBADA'

print validate_password_requirement(password)
