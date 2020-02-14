# metro
Backend for urbanista.mx

#### First Time Usage:

##### Build and start server
`$ docker-compose up --build`

##### Create admin user
`$ docker-compose run app sh -c 'python manage.py createsuperuser'`

Enter desired username, email address and password.

#### Start Up: 
`$ docker-compose up`

On your browser head to: `http://localhost:8000/admin`