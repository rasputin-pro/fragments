# Fragments
![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?logo=sqlite&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?logo=postgresql&logoColor=white)
___
Учебный проект на базе фреймворка **Django** (Frontend & Backend).

Fragments — многопользовательский блог. Проект предоставляет
зарегистрированным пользователям публиковать записи, подписываться на
любимых авторов и отмечать понравившиеся публикации.

## Стек технологий:
- Python 3.7
- Django 2.2.28
- PostgreSQL
- Docker
- Nginx

## Подготовка к работе:
Для работы требуется [poetry](https://python-poetry.org/docs/).
Если ещё не установили, это можно сделать командой:
```bash
curl -sSL https://install.python-poetry.org | python -
```
Клонируйте репозиторий и перейдите в директорию проекта
```bash
git clone git@github.com:rasputin-pro/fragments.git
cd fragments
```

## Как запустить проект:

---
<details>
    <summary><b>Локально через консоль:</b></summary>

1. Создайте и активируйте виртуальное окружение
```bash
poetry config virtualenvs.in-project true
poetry shell
```
2. Установите зависимости
```bash
poetry install --extras "tests"
```
> Дополнительные аргументы: `--extras`
>
> `tests` - для установки библиотек тестирования
3. Примените миграции
```bash
python yatube/manage.py migrate
```
4. В файле `/yatube/yatube/settings.py` смените значение переменной
`STATE` на `local`
5. Запустите программу
```bash
python yatube/manage.py runserver
```
> После запуска проект будет доступен по адресу: http://localhost:8000 и
> http://127.0.0.1:8000
</details>

---

<details>
    <summary><b>Локально через Docker:</b></summary>

Требуется установленный Docker! Зависимости будут установленны из файла
`requirements.txt`
1. Перейдите в папку `infra_local`
2. Создайте файл `.env`. Например:
```dotenv
SECRET_KEY='e)g}6wSknB%G1T/LY^E)#tFd@2cq@(6m^}.c2{7wP88#^-uFZ.'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=fGYWqrGsEQojcDg8
DB_HOST=db
DB_PORT=5432
```
3. В файле `/yatube/yatube/settings.py` смените значение переменной `STATE` на `docker`
4. Выполните команду:
```bash
docker compose up -d
```
> После запуска проект будет доступен по адресу: http://localhost
</details>

---

## Тестирование:
Тесты запускаются локально через консоль командой `pytest` из корня проекта.
> В файле `/yatube/yatube/settings.py` значение переменной `STATE` должно быть: `local`

Для контроля за кодом используйте pre-commit:
```bash
pre-commit install
```

## Планы по развитию проекта:
Проект планируется развивать с целью изучения возможностей Django.
- Разместить сайт на боевом сервере;
- Добавить возможность назначать публикациям множественные категории;
- Реализовать комментарии к публикациям;
- ...
