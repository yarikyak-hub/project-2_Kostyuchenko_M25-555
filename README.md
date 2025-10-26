# Project 2 - Database System
## Author: Kostyuchenko M25-555

Educational database project with command-line interface for table management.

## Демонстрация работы База Данных

https://asciinema.org/a/8RQGS19ipwfFk6J6X4DO1YE39

## Демонстрация работы адаптируем модуль База Данных

https://asciinema.org/a/TFU9wnLMarYbYBa5CTEjMxheT

## Демонстрация работы декораторов



### Обработка ошибок с декоратором `@handle_db_errors`

Система автоматически обрабатывает следующие типы ошибок:

- **KeyError** - обращение к несуществующим таблицам или ключам
- **ValueError** - ошибки валидации типов данных
- **FileNotFoundError** - отсутствие файлов данных
- **Общие исключения** - любые непредвиденные ошибки

## Установка зависимостей
```bash
make install
