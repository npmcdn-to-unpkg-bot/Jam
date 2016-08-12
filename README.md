# Jam
Personal Website 
Personal Music Catalogue
Django App for Recommending New Music

### Deploying Project Locally

After cloning and prior to starting the Django Development Server, you must first install the require dependcies using the command: 

`(myproject_env)$ pip install -r requirements.txt`

To start the Django Development Server run command:

`(myproject_env)$ python3 manage.py runserver`

  **Note:**
  Parts of this project are dependent on running the server in Python 3 (which is what I have defined in my runtime.txt file) instead of 2.7, particularly, in pitchfork_api.py, which uses an imported package named `pitchfork` that does not work with Python 2.*. You may find more about the issues involving that particular package [here](https://github.com/michalczaplinski/pitchfork).

In your browser of choice, visit URL: http://127.0.0.1:8000/time/

### Extraneous yet Important details about the project outside this repo

I have excluded all of my static files from this repo and they only exist locally on my computer and hosted on my [website](www.evancarter.me) which is deployed on Heroku.

I have also excluded my SQLite database binary files, which contain all the existing tables and entry rows necessary to fully see the functionality of this application such as serving specific content of individual album reviews, album covers, and (at some point soon) profile details.

The purpose of these files here are to 1) first and foremost serve my version control needs 2) show the architecture and implementation of Django Framework features I have used and be of use to anyone to explore.

