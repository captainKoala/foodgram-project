# FOODGRAM

## Описание проекта
Foodgram - API и онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Foodgram является дипломным проектом в рамках курса "Python-разработчик" в [Яндекс.Практикум](https://praktikum.yandex.ru/).

## Запуск проекта
Для запуска проекта необходимо из директории `/infra` выполнить команду:
```
docker-compose up
```

Сайт сервиса будет доступен по адресу: http://localhost.

Корень API доступен по адресу: http://localhost/api/.

Спецификация API доступна по адресу: http://localhost/api/docs/.

Административная панель доступна по адресу: http://localhost/admin/.

## Пример
Сайт доступен по адресу http://foodgram.koalavisit.ru.

Панель администратора доступна по логину `admin` и паролю `password1234example`. 

## Используемые технологии для построения API

* Django
* Django Rest Framework
* Djoser