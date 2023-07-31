# Проект Yatube

[![CI](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml)

Yatube - это проект Социальной сети, которая позволяет пользователям просматривать интересный контент, который пишут различные авторы. Вы также можете стать автором и подписываться на других пользователей, чтобы следить за обновлениями их контента. Кроме того, вы можете объединяться в сообщества по интересам.

## Стек технологий

- Python
- Django
- Docker
- PostgreSQL
- Gunicorn
- Nginx

## Особенности проекта

- Регистрация и аутентификация пользователей
- Просмотр, создание и редактирование постов
- Возможность оставлять комментарии под постами
- Подписка на авторов и просмотр их контента
- Создание сообществ и присоединение к ним
- Поиск по постам и авторам
- Интерактивная лента с новыми постами от подписанных авторов
- API для интеграции с другими приложениями

## Запуск проекта

1. Склонируйте репозиторий:
```
git clone https://github.com/Leenominai/hw05_final.git
```
2. Создайте и активируйте виртуальное окружение:
```
python -m venv venv
venv/bin/activate
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Выполните миграции:
```
python manage.py makemigrations
python manage.py migrate
```
5. Запустите сервер:
```
python manage.py runserver
```
6. Теперь вы можете открыть проект в браузере по адресу http://localhost:8000/ и начать использовать YAMDB!
