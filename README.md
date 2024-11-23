# DjangoCarsComments
Реализация REST API для управления отзывами на автомобили. Тестовое задание. Используемые технологии: Django, Django Rest Framework, Docker

# How to run localy

### git clone this project
```
github.com/deomore/TestDjango.git
set "master" branch 
```

### Set your database settings
1. Replace some database configuration settings with your data
```
NAME = 'cars_db' 
USER = 'root'
PASSWORD = 'root'
HOST = 'localhost' *
PORT = '5432'  *

* - usually stay same 
```
2. Create database tables
```
python manage.py migrate
```

### Install requirements
```
pip install -r requirements.txt
```

### Run server
```
python manage.py runserver
```

# How to run with docker

### git clone this project
```
github.com/deomore/TestDjango.git
set "docker`ed" branch 
```

### Docker settings
1. Setup your ENV files for each service (API + db)
here is example
```
POSTGRES_DB=cars
POSTGRES_USER=car_admin
POSTGRES_PASSWORD=cars1234
POSTGRES_HOST=db
POSTGRES_PORT=5432

```
2. Set up ports in docker-compose
If u dont have postgres localy or port is unused for some other reasons - skip this
```
    ports:
      - "5432:5432"
```
application port is 8080 by default 
```
       ports:
      - "8000:8000"
```

3. Change default superuser settings in dockerfile with credits you want
```
      python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" 
```
   

### Compose it up
```
docker compose up
```



# Authentication
This service use TokenAuthentication.

### How to get token
Request
```
curl -X POST http://127.0.0.1:8000/api/token/auth/
   -H "Content-Type: application/json"
   -d '{"username": "your_username", "password": "your_password"}'  
```

Response
```
{
    "token": "d5ab43865024343e77358566917d5a30a37059cd"
}
```


### Api Endpoints anabled without auth token
 - /api/counties/ GET
 - /api/brands/ GET
 - /api/cars/ GET
 - /api/comments/ GET
 - /api/comments/ POST
 - /api/comments/download/ GET

### Api Endpoints with auth token required
  - /api/counties/ POST 
  - /api/counties/<int:country_id>/ PUT 
  - /api/counties/<int:country_id>/ DELETE

  - /api/brands/ POST 
  - /api/brands/<int:brand_id>/ PUT 
  - /api/brands/<int:brand_id>/ DELETE

  - /api/cars/ POST 
  - /api/cars/<int:car_id>/ PUT 
  - /api/cars/<int:car_id>/ DELETE

  - /api/comments/<int:comments_id>/ PUT 
  - /api/comments/<int:comments_id>/ DELETE 



