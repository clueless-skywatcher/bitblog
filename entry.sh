if [ -d "media" ]
then 
    rm -Rf media
fi

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000