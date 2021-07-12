## internhacks-team11

### Setup Instructions:
Clone Github repo to your local computer:
`$ git clone git@github.com:kharissa/internhacks-team11.git`

### Requirements:
- Check Python3 is installed:
`$ python3 —version`
- Setup virtual environment:
`$ python3 -m venv venv`
`$ source venv/bin/activate`
- Install Flask:
`$ python3 -m pip install Flask`
- Install project requirements:
`$ python3 -m pip install -r requirements.txt`
- Create .env file (should be on same level as your run.py file). Enter the following:
`SECRET_KEY='ENTER_SECRET_KEY_HERE'`
- Confirm you can run the server:
`$ python3 run.py`

### Important Information:
- If you install packages, make sure to save the package in the requirements.txt so that your team members can easily install and run with each fresh pull to the remote branch:
`$ python3 -m pip freeze > requirements.txt`
- If you want your changes to be automatically shown when developing, type this into your command line:
`$ FLASK_ENV=development flask run`

### Before Coding:
- Create and switch to new local branch (no spaces):
`$ git checkout -b BRANCH_NAME`
- Check what files have changed:
`$ git status`
- Add files in the working tree to be staged
`$ git add`
- Save or commit files 
`$ git commit -m "COMMIT_MESSAGE"`
- Push your locally committed files to the remote branch
`$ git push`
`$ git push --set-upstream origin CreateDatabase` # the first time you do this
- Pull the most recent changes to your local
`$ git pull`

### Setting up NEW Database
- Open Python3:
`from internhacks import db`
`db.create_all()`
`from models import User`
`user1 = User(username='USERNAME', email='EMAIL_ADDRESS', password='PASSWORD')`
`user1 = User(username='kharissa', email='kharissa@test.com', password='password')`
`db.session.add(user1)`
`db.commit.all()`

### SQL Queries
- Return list of users
`User.query.all()`
- Return user by username
`User.query.filter_by(username='USERNAME').first()`
- Return user by ID
`User.query.get(ID)`
