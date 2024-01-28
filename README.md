# Магазин:

## Технологии:
-  Python, Django, Postgres, Bootstrap, CSS, Celery, Redis, Pandas.
## Web интерфейс:
- Bootstrap ,CSS.
## Ссылки:
- https://github.com/Dmitrii-ru/Dekor_shop
## Реализованные решения:
- Асинхронные фоновые задачи, кастомизация административной панели, ручное кэширование, оптимизация запросов, 
фильтрация и ранжирование по релевантности запросу, парсинг macros excel каталога, предварительное валидирование данных каталога, 
резервное копирование части базы данных.

## Приложения
### Магазин
- Прилавок продуктов (Категории, группы, продукты)
- Поисковая система
  -  Фильтрация и ранжирование по релевантности запроса, индексация полей, подготовка базовых форм слов
- Кастомизация административной палеи
  - Разграничение прав доступа
  - fieldsets, изображения, вычисляемые поля

### Инструменты сайта
- Загрузка каталога, предварительное валидирование данных каталога
  - Транзакционная загрузка каталога
  - Парсинг macros excel, получение уровней вложенности
  - Динамический механизм валидирования на основе ООП данных
    - Базовый класс, классы для методов (Update, Create), класс моделей 
  - Информирование пользователя какое поле у объекта не прошло валидацию или на какой этапе произошла ошибка
  - Подготовка отчета о загрузке для каждой модели в excel формате
  - Подготовка базовых форм слов для SearchVector
  - Динамическое групповое обновление полей объектов
  - Оптимизация заботы с базой данных
  - Возможность восстановить базу данных 

## Команды для запуска 
### Redis
  * pip install redis==4.6.0
  * redis-server --daemonize yes

### Postgres
  * pip install postgres
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
   * poetry init
   * poetry add $(cat requirements.txt)
   * poetry shell
   * python3 manage.py makemigrations
   * python3 manage.py migrate
   * python3 manage.py createsuperuser
  
### Запуск Django
  * python3 manage.py runserver

### Запуск Celery worker
  * celery -A core worker -B -Q shop
  * celery -A core worker -B -Q site_tools
  * celery -A core worker -B
    