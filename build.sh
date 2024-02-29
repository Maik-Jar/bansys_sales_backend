#!/usr/bin/env bash
# exit on error
set -o errexit

# pip install --upgrade pip
# pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata initial_data/documentType_initial_data.json 
python manage.py loaddata initial_data/customer_initial_data.json 
python manage.py loaddata initial_data/paymentMethod_initial_data.json 
python manage.py loaddata initial_data/tax_initial_data.json
python manage.py loaddata initial_data/receipt_initial_data.json 
python manage.py loaddata initial_data/saleType_initial_data.json 
python manage.py createsuperuser --username brivera --email maikrivera01@gmail.com --noinput
python manage.py runserver
