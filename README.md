# Fragments
![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?logo=sqlite&logoColor=white)
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

## Как запустить проект:

---
<details>
    <summary><b>Локально через консоль:</b></summary>

1. Клонируйте репозиторий
```commandline
git clone git@github.com:rasputin-pro/fragments.git

cd fragments
```
2. Создайте и активируйте виртуальное окружение
```bash
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip

# Windows
python -m venv venv
source venv/scripts/activate
python -m pip install --upgrade pip
```
> В проекте используется **Python** версии **3.7**
3. Установите зависимости из файла `requirements.txt`
```bash
pip install -r requirements.txt
```
4. Примените миграции
```bash
# Linux/MacOS
python3 yatube/manage.py migrate

# Windows
python yatube/manage.py migrate
```
5. Запустите программу
```bash
python3 yatube/manage.py runserver
```
</details>

---

<details>
    <summary><b>Локально через Docker:</b></summary>

1. Перейдите в папку infra_local
2. Создайте файл `.env`
</details>

---

## Планы по развитию проекта:
Проект планируется развивать с целью изучения возможностей Django.
- Интегрировать CD/CI;
- Разместить сайт на боевом сервере;
- Добавить возможность назначать публикациям множественные категории;
- Реализовать комментарии к публикациям;
- ...
