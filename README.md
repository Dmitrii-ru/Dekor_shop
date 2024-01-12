# Магазин:

___

# APPS :

### - `core` Настройки сайта
- Настройки сайта и сторонних библиотек. 

___

### - `shop` Прилавок магазина
- Предоставление информации об ассортименте магазина. 

___

### - `site_tools` Внутренние инструменты и сервисы сайта
- Загрузка каталога.
##### подробнее : `/site_tools/readme_app.md`
___

## Команды для запуска 
### Redis
  * pip install redis==4.6.0
  * redis-server --daemonize yes

### Postgres
  * pip install postgres==14.10 
  * sudo -u postgres psql
    * CREATE DATABASE shop;
    * CREATE USER shop_user WITH PASSWORD 'shop_user_password';
    * ALTER ROLE shop_user SET client_encoding TO 'utf8';
    * ALTER ROLE shop_user SET default_transaction_isolation TO 'read committed';
    * ALTER ROLE shop_user SET timezone TO 'UTC';
    * GRANT ALL PRIVILEGES ON DATABASE shop TO shop_user;
    * \q
  * sudo --login -u postgres psql

### ENV
- Создать файл .env в корне 
    * SECRET_KEY='input_key'
    * NAME_DB='shop'
    * USER_DB='shop_user'
    * PASSWORD_DB='shop_user_password'
    * HOST_DB='localhost'

### Подготовка Django
   * python3 -m venv venv 
   * source venv/bin/activate
   * pip install -r requirements.txt
   * python3 manage.py makemigrations
   * python3 manage.py migrate
   * python3 manage.py createsuperuser
  
### Запуск Django
  * python3 manage.py runserver

### Запуск Celery worker
  * celery -A core worker -B


