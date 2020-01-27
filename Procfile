web: gunicorn myapp.wsgi 0.0.0.0:5000 --log-file -
migrate: python manage.py migrate --settings=myapp.settings.production
seed: python manage.py loaddata myapp/item/data/fixtures/items-data.json