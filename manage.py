# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from BookSwap import app

'''
This script is used for locally modifying the database. Say you want to add
some users to the database, you can run 'python manage.py shell' to open up
a shell that will let you interact with the DB through the Flask application.

Sample shell interaction:

$ python manage.py shell

>>> from database.models import *
>>> user = User(
... email='danielmac@gmail.com',
... password='somepass',
... activated=False)
>>> user
<User: User object>
>>> user.save()
<User: User object>
>>> users = User.objects.get()
>>> users
<User: User object>
>>> users.email
u'danielmac@gmail.com'
'''


manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)


if __name__ == "__main__":
    manager.run()

