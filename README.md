# Project 2 - Database System
## Author: Kostyuchenko M25-555

Educational database project with command-line interface for table management.

## Демонстрация работы База Данных

https://asciinema.org/a/8RQGS19ipwfFk6J6X4DO1YE39

## Демонстрация работы адаптируем модуль База Данных

https://asciinema.org/a/TFU9wnLMarYbYBa5CTEjMxheT

## Демонстрация работы декораторов

https://asciinema.org/a/PkdaEyw3abzIEpfmvrfE1R8Q8

### Обработка ошибок с декоратором `@handle_db_errors`

## Запуск базы данных
# После установки через pipx
database
# Или через poetry (режим разработки)
poetry run database

Система автоматически обрабатывает следующие типы ошибок:

- **KeyError** - обращение к несуществующим таблицам или ключам
- **ValueError** - ошибки валидации типов данных
- **FileNotFoundError** - отсутствие файлов данных
- **Общие исключения** - любые непредвиденные ошибки

## Неверный тип вводимых данных, где 'none' должно быть число
Введите команду: insert clothes scarf none 333 blue true
Функция load_table_data выполнилась за 0.000 секунд.
Ошибка валидации: Неверный тип для столбца 'size'. Ожидается int

## Подтверждение удаления строки из таблицы
Введите команду: delete clothes where "ID = 3"
Функция load_table_data выполнилась за 0.000 секунд.
Вы уверены, что хотите выполнить "удаление записей"? [y/n]: y
Удалено записей: 1
Функция delete выполнилась за 4.028 секунд.
