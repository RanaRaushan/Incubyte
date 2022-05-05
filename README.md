# Incubyte

Deployment Link for the [Incubyte Word app](https://incubytes-app.herokuapp.com/word)

Basic Info: This app has been using python language, and API has been handled via [FastAPI](https://fastapi.tiangolo.com/)

Following are the structure of the project.

1. db (Contain database file which handle connection and creating db tables)
	- database.py
2. templates (These are the html templates that is used to show on FrontEnd side)
	- HomePage.html
	- update_word.html
3. word_app (This is word app which contains all files related to app and test for this app as well)
	- test (This is test module for the word app that will can run for unittest)
		- conftest.py
		- test_utils.py
		- test_word_app.py
	- exception.py
	- models.py
	- routes.py
	- schemas.py
	- words.py
4. main.py (This is main file where initially API has been created and submodule has been divided on above part)
5. Procfile (This is one of the file that is required for deploying on heroku )
6. requirements.txt (All the imported library has been stored to run on heroku app while deploying)

