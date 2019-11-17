# ipi_stats
IPL stats endpoints

Install Docker, pull repository then

Create .env files with below variables

For .env example

    DEBUG=0
    SECRET_KEY=p!e6j0+md()f=)v_*@7j2g67!f!i&c40e9vi4o+0ka6d0+rf4(
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] 0.0.0.0
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=ipl_db
    SQL_USER=ipl_usr
    SQL_PASSWORD=ipl_db__
    SQL_HOST=db
    SQL_PORT=5432

Then run compose file, followed with migration and loading the data given in CSV 

    sudo docker-compose up --build -d
    sudo docker-compose exec web python manage.py migrate
    sudo docker-compose exec web python manage.py load_data
