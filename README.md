# internhacks-team11

## Setup Instructions:
Clone Github repo to your local computer:
`git clone git@github.com:kharissa/internhacks-team11.git`

## Requirements:
- Check Python3 is installed:
`$ python3 —version`
- Setup virtual environment:
`$ python3 -m venv venv`
`$ source venv/bin/activate`
- Install Flask:
`$ python3 -m pip install Flask`
- Install project requirements:
`python3 -m pip install -r requirements.txt`
- Confirm you can run the server:
`export FLASK_APP=server.py`
`flask run`

## Important Information:
- If you install packages, make sure to save the package in the requirements.txt so that your team members can easily install and run with each fresh pull to the remote branch:
`python3 -m pip freeze > requirements.txt`

## Before Coding:
- Create and switch to new local branch (no spaces):
`git checkout -b BRANCH_NAME`
- 