init:
	python3 src/py_challenge_flask/utils/db_init.py

dev:
	FLASK_APP=./src/py_challenge_flask/main.py FLASK_ENV=development flask run
