## Описание
Этот модуль предназначен для парсинга расписания с сайта физфака и загрузки его в базу данных.

## Использование
Сперва нужно отредактировать файл ````T.py````. Параметр at - токен авторизации в тестовую БД. Затем указать параметры соеднинения (host, database ...) для взятия данных
из таблицы, имитирующей сайт расписания (это временная мера, поскольку летом расписание физфака пусто).
```sh
at = "some_token"
host = "localhost"
database = "postgres"
user = "postgres"
password = "postgres"
```

Далее нужно отредактировать сам скрипт ````main.py````, указав дату начала периода загрузки и конца:
```sh
be = datetime.datetime.now()
begin = be.strftime("%m/%d/%Y")
en = datetime.datetime.now() + datetime.timedelta(days=2)
end = en.strftime("%m/%d/%Y")
```
После этого ````main.py```` можно запускать.

## Зависимости
1. Pandas;
2. Requests;
3. Retrying;
4. BeautifulSoup4;
5. Setuptools;
