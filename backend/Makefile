.PHONY: install setup fake developmentsuperuser runserver default

default: install setup fake developmentsuperuser runserver

install:
	pip install -r requirements.txt

setup:
	python manage.py makemigrations users jobs

	python manage.py migrate

	python manage.py collectstatic

fake:
	python -m api fake all

developmentsuperuser:
	python manage.py createsuperuser --username developer \
	 --email localhost@admin.com --category Individual \
	  --description "Site admin" --location localhost \
	  --phone_number +254700000000 --noinput

runserver:
	python -m api run