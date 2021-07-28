# collect static files
python manage.py collectstatic --no-input

sleep 10

echo "Applying migrations"
python manage.py migrate

# start django server
#python manage.py runserver 0.0.0.0:8002

# start server with gunicorn
gunicorn --reload sample-survey.wsgi:application 0.0.0.0:8002
