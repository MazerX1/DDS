# DDS
# Веб-сервис ДДС

## Инструкция по запуску проекта

### 1. Установка зависимостей
1. Установите **Python 3.10+** и **pip**.  
2. Клонируйте репозиторий:
   git clone (https://github.com/MazerX1/DDS)
   cd DDS
3. Создайте виртуальное окружение:
   python -m venv venv
  source venv/bin/activate   # Linux/MacOS
  venv\Scripts\activate      # Windows
4. Установите зависимости:
   pip install -r requirements.txt
   
### 2. Настройка базы данных
1. По умолчанию используется SQLite, который встроен в Python.
2. В проекте база данных обычно хранится в файле db.sqlite3 (создаётся автоматически при миграциях).
3. Если хотите использовать другую БД — измените настройки в settings.py в блоке DATABASES.

### 3. Применение миграций
Выполните команды для создания структуры базы данных:
  python manage.py makemigrations
  python manage.py migrate

### 4. Создание суперпользователя
Для входа в админ-панель:
  python manage.py createsuperuser

### 5. Запуск веб-сервиса
Запустите сервер:
  python manage.py runserver
После запуска сервис будет доступен по адресу:
👉 http://127.0.0.1:8000
