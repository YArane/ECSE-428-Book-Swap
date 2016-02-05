# ECSE-428-Book-Swap

A web-platform to facilitate textbook exchanges amongst the McGill community. 

If you have a better suggestion to any of the things I'm proposing here, please let us all know about them! I don't want anyone to feel like I'm Hugo Chavez setting all the rules.

# Setup and Other Recommended Things

## IDE ##

- You can use PyCharm as the IDE for the project (https://www.jetbrains.com/pycharm/). It has some great features that will help you write and learn python (e.g. code completion). Go on the website and get a student license for a year.

## PIP ##

- PIP is a package manager for Python. It's like NPM or Bower for javascript. You should aready have it installed on your computer - Open up a terminal and run `pip` to see if the command exists. Follow the installation instructions if you don't have it (https://pip.pypa.io/en/stable/installing/).

## Virtualenv ##

Virtualenv is an awesome tool for mananging dependencies for a python project. We will use it to make sure that we are all *always* working with the same set of tools. 

- To install virtualenv in OSX follow steps 1 to 4 of the following page (ignore all the remaining steps): http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/

- To install virtualenv on Linux follow step 8 of the following page (ignore all the other steps): http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/

## MongoDB ##

We are using MongoDB as the data store for the project. Once we start building the DB endpoints (right now), you'll need to have MongoDB installed on your computer to run the webserver. 

- Ubuntu installation instructions: https://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/
- Mac OS X installation instructions: https://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/
- Windows installation instructions: https://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/
- Ask Katie or Daniel to help you setup a local db on your computer. Here are quick instructions:

1. Make a folder somewhere on your computer to store the data. Please DO NOT make it inside the repository folder, you shouldn't push your DB to the repo.

  `mkdir bookswap_data`
  
2. Create and bootup a MongoDB instance (terms totally made up by me, Daniel):

  `mongod --dbpath bookswap_data`
  
3. You should see a process run on that terminal window. Great, you have a database locally deployed on your computer. Now you can open a second terminal and use the mongo command to explore your db (you need a new window, leave the DB running). You need to run the mongo command while inside the bookswap_data folder
  
  `cd bookswap_data`

  `mongo`
  
4. Follow this guide to do cool things on your DB (insert, update, remove, ...): https://docs.mongodb.org/manual/reference/mongo-shell/

5. Rejoice in your abilities to install dependencies. This is what you were born for. I'm sure someone will hire you because you have truly mastered the craft of googling tutorials.

## Project Setup ##

Follow these steps to begin coding:

1. Clone this repository 

  `git clone https://github.com/YArane/ECSE-428-Book-Swap`

2. Go into the folder

  `cd ECSE-428-Book-Swap`

3. Create a new virtualenv for the project. You will automatically be using it by running this command. If you want to stop using it run `deactivate`, and to start using it again run `workon bookswap`.

  `mkvirtualenv bookswap`

  For Windows, you can initialize the folder for the virtual environment by running this command. You can activate the virtualenv by running 'activate' from the folder's Scripts directory.

  `virtualenv bookswap`

3. Install the dependencies by running the following (the file requirements.txt contains a list of all the dependecies used by the project)
  
  `pip install -r requirements.txt`

4. Follow the MongoDB instructions explained in the section above. Note that you don't have to follow step 3, that is just for playing around with MongoDB. If you don't complete steps 1 and 2, running the server will fail.

5. Run the server to verify that everything is OK. Your terminal should say `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`. You can run the URL in your browser to see the BookSwap index page.

  `python BookSwap.py`
  
6. Rejoice in your success.

# Coding Conventions #

Some random things that would really add value if you follow them while you code.

## Style ##

I think we should follow this guide: https://github.com/amontalenti/elements-of-python-style - I ONLY care about these naming conventions, the rest are nice-to-haves:

- Class names: CamelCase, and capitalize acronyms: HTTPWriter, not HttpWriter.
- Variable names: lower_with_underscores.
- Method and function names: lower_with_underscores.
- Modules: lower_with_underscores.py. (But, prefer names that don't need underscores!)
- Constants: UPPER_WITH_UNDERSCORES.
- Precompiled regular expressions: name_re.

## Git Commits ##

Keep your commit messages relevant to what you are pushing (messages can be really useful!). I follow the convention of writing them in present tense: "Add endpoint for listing retrieval" instead of "Added endpoint for listing retrieval".
