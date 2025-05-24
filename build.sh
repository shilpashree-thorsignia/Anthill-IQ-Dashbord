#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput 
python manage.py runserver --settings=anthill_iq.settings