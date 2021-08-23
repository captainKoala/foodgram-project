# FOODGRAM

## Описание проекта
Foodgram - API и онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Foodgram является дипломным проектом в рамках курса "Python-разработчик" в [Яндекс.Практикум](https://praktikum.yandex.ru/).

## Запуск проекта
Для запуска проекта необходимо из директории `/infra` выполнить команду:
```
docker-compose up
```

Далее необходимо сделать миграции базы данных и собрать статику:

```
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input 
```
Создание суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
При необходимости можно загрузить тестовые данные (файл `dump.json` находится в 
директории `data/`, поэтому его необходимо предварительно скопировать в 
директорию `backend/`):
```
docker-compose exec web python manage.py loaddata dump.json
```
Сайт сервиса будет доступен по адресу: http://localhost.

Корень API доступен по адресу: http://localhost/api/.

Спецификация API доступна по адресу: http://localhost/api/docs/.

Административная панель доступна по адресу: http://localhost/admin/.

## Пример
Сайт доступен по адресу http://foodgram.koalavisit.ru.

## Используемые технологии для построения API

* Django
* Django Rest Framework
* Djoser
