# Система опроса пользователей

## Документация

Документация доступна по ссылкам:

- /redoc/
- /swagger/

## Регистрация пользователей

Используется [djoser](https://djoser.readthedocs.io/).

Для регистрации пользователя отправьте логин и пароль POST-запросом на `/auth/users/`. Логин и пароль
передаются соответственно в полях `username` и `password` тела запроса. В случае успеха вернётся HTTP-ответ со статусом `201 Created`.

Для получения токена отправьте POST-запрос на `/auth/jwt/create/`, передав действующий логин и пароль в полях `username` и `password`.

Токен передается в заголовке каждого запроса, в поле `Authorization`. Перед самим токеном необходимо добавить ключевое слово `Bearer` с последующим пробелом.

## Замечания касательно версий пакетов

# Django

Вместо версии `2.2.10`, прописанной в ТЗ, используется версия `2.2.16`. Это сделанно для корректной работы пакета `drf-yasg` (версии `1.20.0`).

# psycopg2

Используется версия `2.8.6`, т.к. версия `2.9.1` приводит к `AssertionError: database connection isn't set to UTC`.

## Установка Postgresql

```
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
postgres=# ALTER USER postgres PASSWORD 'postgres';
````
