.PHONY: install setup fake test test-api-v1 developmentsuperuser runserver default

default: install setup fake developmentsuperuser runserver

install:
	pip install -r requirements.txt

setup:
	python manage.py makemigrations users jobs


	python manage.py migrate

	python manage.py collectstatic

fake:
	python -m api fake all

test: test-api-v1

test-api-v1:
	pytest api/tests/test_v1.py -xv

developmentsuperuser:
	python manage.py createsuperuser --username developer \
	 --email developer@localhost.domain --category Individual \
	  --description "Site developer" --location localhost \
	  --phone_number +254700000000 --noinput

runserver:
	python -m api run