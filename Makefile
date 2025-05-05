run:docker-compose up --build
stop:docker-compose down
migrate:docker-compose run django python manage.py migrate
createsuperuser:docker-compose run django python manage.py createsuperuser
collectstatic:docker-compose run django python manage.py collectstatic --noinput
