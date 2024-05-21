#!/usr/bin/env bash
# exit on error
set -o errexit

apt-get update && \
apt-get install -y locales && \
sed -i -e 's/# es_DO.UTF-8 UTF-8/es_DO.UTF-8 UTF-8/' /etc/locale.gen && \
dpkg-reconfigure --frontend=noninteractive locales

pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata initial_data/documentType_initial_data.json 
python manage.py loaddata initial_data/customer_initial_data.json 
python manage.py loaddata initial_data/paymentMethod_initial_data.json 
python manage.py loaddata initial_data/tax_initial_data.json
python manage.py loaddata initial_data/receipt_initial_data.json 
python manage.py loaddata initial_data/saleType_initial_data.json 
python manage.py createsuperuser --username brivera --email maikrivera01@gmail.com --noinput
# python manage.py runserver
