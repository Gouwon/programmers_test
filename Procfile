web: gunicorn myapp.wsgi 0.0.0.0:5000 --log-file -
migrate: /bin/true
seed: python manage.py loaddata myapp/item/data/fixtures/items-data.json