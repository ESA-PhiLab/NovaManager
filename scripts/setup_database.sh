#python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuser
#cat scripts/update_machines.py | python manage.py shell
