## Описание
Этот модуль предназначен для парсинга расписания с сайта физфака и загрузки его в базу данных.

## Использование
Запуск осуществляется через командную строку:
```sh
python3 semester.py -h
```
Данная строчка выведет в консоль helper-файл, в котором описаны все существующие параметры.

При работе программы предусмотрено логгирование важной информации. Например, в консоль будут выводиться те пары, для которых не нашлось подходящего регулярного выражения:
````sh
INFO - Начинаю парсить 'name'...
WARNING - Для '429 - С/К по выбору доц. Водовозов В. Ю.' не найдено подходящее регулярное выражение.
WARNING - Для '229М - С/К по выб доц. Водовозов В. Ю.' не найдено подходящее регулярное выражение.
````

Или, например:
```sh
INFO - Превращаю преподавателей в id...
CRITICAL - Ошибка, преподаватель 'Водовозов В. Ю.' не найден. Завершение работы
```

## Зависимости
1. Pandas;
2. Requests;
3. Retrying;
4. BeautifulSoup4;


## Скрипты
В проекте есть папка scripts. В ней хранятся единоразово используемые скрипты. Качество кода в них не контролируется. 

Это существует ради сохранения кода.
