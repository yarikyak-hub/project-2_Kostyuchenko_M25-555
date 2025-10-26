import shlex
from prettytable import PrettyTable
from .utils import (load_metadata, save_metadata, create_table, drop_table, 
load_table_data, save_table_data)
from .core import insert, select, update, delete, clear_select_cache
from .parser import parse_where, parse_set


def list_tables(metadata):
    """Показывает список всех таблиц"""
    if "tables" not in metadata or not metadata["tables"]:
        print("В базе данных нет таблиц")
        return
    
    print("Таблицы в базе данных:")
    for table_name, table_info in metadata["tables"].items():
        columns = [f"{col[0]}:{col[1]}" for col in table_info["columns"]]
        print(f"  {table_name}: {', '.join(columns)}")


def welcome():
    """Функция приветствия"""
    print("***")
    print("Primitive Database System")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    print("<command> create_table <table_name> <column1:type1>"
    " [column2:type2 ...] - создать таблицу")
    print("<command> drop_table <table_name> - удалить таблицу")
    print("<command> list_tables - показать все таблицы")
    print("<command> insert <table_name> <value1> <value2> ... - добавить запись")
    print("<command> select <table_name> [where условие] - выбрать записи")
    print("<command> update <table_name> set <set_условие>"
    " [where <where_условие>] - обновить записи")
    print("<command> delete <table_name> [where <where_условие>] - удалить записи")


def print_table_result(table_data, columns):
    """
    Выводит данные таблицы в красивом формате с помощью PrettyTable.
    
    Args:
        table_data (list): Данные таблицы
        columns (list): Список столбцов в формате [("name", "type"), ...]
    """
    if not table_data:
        print("Нет данных для отображения")
        return
    
    # Создаем таблицу
    table = PrettyTable()
    
    # Устанавливаем заголовки
    field_names = [col[0] for col in columns]
    table.field_names = field_names
    
    # Добавляем данные
    for record in table_data:
        row = [record.get(field, "") for field in field_names]
        table.add_row(row)
    
    # Настраиваем внешний вид
    table.align = "l"  # Выравнивание по левому краю
    
    print(table)
    print(f"Всего записей: {len(table_data)}")


def run():
    """Главная функция с основным циклом программы"""
    welcome()
    metadata_file = "db_meta.json"
    
    while True:
        # Загружаем актуальные метаданные
        metadata = load_metadata(metadata_file)
        
        try:
            user_input = input("Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы. До свидания!")
            break
            
        if not user_input:
            continue
            
        # Разбираем введенную строку на команду и аргументы
        args = shlex.split(user_input)
        command = args[0].lower() if args else ""
        
        if command == "exit":
            print("Выход из программы. До свидания!")
            break
            
        elif command == "help":
            welcome()
            
        elif command == "list_tables":
            list_tables(metadata)
            
        elif command == "create_table":
            if len(args) < 3:
                print("Ошибка: Используйте: create_table <table_name>"
                " <column1:type1> [column2:type2 ...]")
                continue
                
            table_name = args[1]
            columns_spec = args[2:]
            
            # Парсим(извлекаем) спецификации столбцов
            columns = []
            for col_spec in columns_spec:
                if ":" not in col_spec:
                    print(f"Ошибка: Неверный формат столбца '{col_spec}'."
                    " Используйте name:type")
                    break
                col_name, col_type = col_spec.split(":", 1)
                columns.append((col_name, col_type))
            else:
                new_metadata = create_table(metadata, table_name, columns)
                if new_metadata is not None:
                    if save_metadata(metadata_file, new_metadata):
                        print("Метаданные сохранены в db_meta.json")
                    else:
                        print("Ошибка при сохранении метаданных")
                    
        elif command == "drop_table":
            if len(args) != 2:
                print("Ошибка: Используйте: drop_table <table_name>")
                continue
                
            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)
            if new_metadata is not None:
                if save_metadata(metadata_file, new_metadata):
                    print("Метаданные сохранены в db_meta.json")
                else:
                    print("Ошибка при сохранении метаданных")
        elif command == "insert":
            if len(args) < 3:
                print("Ошибка: Используйте: insert <table_name> <value1>"
                " <value2> ...")
                continue
                
            table_name = args[1]
            values = args[2:]
            
            # Проверяем существование таблицы
            if "tables" not in metadata or table_name not in metadata["tables"]:
                print(f"Ошибка: Таблица '{table_name}' не существует!")
                continue
            
            # Вставляем запись
            new_data = insert(metadata, table_name, values)
            if new_data is not None:
                clear_select_cache()
                print("Данные успешно добавлены")
                
        elif command == "select":
            if len(args) < 2:
                print("Ошибка: Используйте: select <table_name> [where условие]")
                continue
                
            table_name = args[1]
            where_clause = None
            
            # Проверяем существование таблицы
            if "tables" not in metadata or table_name not in metadata["tables"]:
                print(f"Ошибка: Таблица '{table_name}' не существует!")
                continue
            
            # Парсим условие WHERE если есть
            if len(args) > 2 and args[2].lower() == "where":
                where_str = " ".join(args[3:])
                where_clause = parse_where(where_str)
                if where_clause is None:
                    continue
            
            # Загружаем данные таблицы
            table_data = load_table_data(table_name, metadata)
            if table_data is None:
                continue
            
            # Выполняем SELECT
            result = select(table_data, where_clause)
            
            # Выводим результат в виде красивой таблицы
            columns = metadata["tables"][table_name]["columns"]
            print_table_result(result, columns)
                    
        elif command == "update":
            if len(args) < 4 or args[2].lower() != "set":
                print("Ошибка: Используйте: update <table_name> set <set_условие>"
                " [where <where_условие>]")
                continue
                
            table_name = args[1]
            
            # Проверяем существование таблицы
            if "tables" not in metadata or table_name not in metadata["tables"]:
                print(f"Ошибка: Таблица '{table_name}' не существует!")
                continue
            
            set_str = " ".join(args[3:])
            
            # Разделяем SET и WHERE части
            where_clause = None
            if " where " in set_str.lower():
                set_part, where_part = set_str.split(" where ", 1)
                set_clause = parse_set(set_part)
                where_clause = parse_where(where_part)
            else:
                set_clause = parse_set(set_str)
            
            if set_clause is None:
                continue
            
            # Загружаем данные таблицы
            table_data = load_table_data(table_name, metadata)
            if table_data is None:
                continue
            
            # Выполняем UPDATE
            updated_data = update(table_data, set_clause, where_clause)
            
            # Сохраняем изменения
            if save_table_data(table_name, updated_data, metadata):
                print("Изменения сохранены")
            else:
                print("Ошибка при сохранении изменений")
                
        elif command == "delete":
            if len(args) < 2:
                print("Ошибка: Используйте: delete <table_name> [where <where_условие>]")
                continue
                
            table_name = args[1]
            
            # Проверяем существование таблицы
            if "tables" not in metadata or table_name not in metadata["tables"]:
                print(f"Ошибка: Таблица '{table_name}' не существует!")
                continue
            
            where_clause = None
            
            # Парсим условие WHERE если есть
            if len(args) > 2 and args[2].lower() == "where":
                where_str = " ".join(args[3:])
                where_clause = parse_where(where_str)
                if where_clause is None:
                    continue
            
            # Загружаем данные таблицы
            table_data = load_table_data(table_name, metadata)
            if table_data is None:
                continue
            
            # Выполняем DELETE
            updated_data = delete(table_data, where_clause)
            
            # Сохраняем изменения
            if save_table_data(table_name, updated_data, metadata):
                print("Изменения сохранены")
            else:
                print("Ошибка при сохранении изменений")
                
        else:
            print(f"Неизвестная команда: '{command}'")
            print("Введите 'help' для справки по командам")
