.PHONY: install setup fake runserver default

default: install setup fake runserver

install:
	pip install -r requirements.txt

setup:
	python manage.py makemigrations users jobs

	python manage.py migrate

	python manage.py collectstatic

fake:
	python -m api fake all

runserver:
	python -m api run