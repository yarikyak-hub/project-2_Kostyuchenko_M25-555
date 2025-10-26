import json
import os
from .decorators import handle_db_errors, confirm_action, log_time


@log_time
@handle_db_errors
def load_metadata(filepath):
    """
    Загружает данные из JSON-файла.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {filepath}: {e}")
        return {}


@log_time
@handle_db_errors
def save_metadata(filepath, data):
    """
    Сохраняет переданные данные в JSON-файл.
    """
    try:
        # Если filepath пустой, используем значение по умолчанию
        if not filepath:
            filepath = "db_meta.json"
            print(f"Предупреждение: Путь к файлу пустой, используется '{filepath}'")
        
        # Создаем директорию, если она не существует (только если есть поддиректории)
        directory = os.path.dirname(filepath)
        if directory:  # Только если путь содержит директории
            os.makedirs(directory, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Метаданные успешно сохранены в {filepath}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}")
        return False

@log_time
@handle_db_errors
def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в метаданных.
    """
    if "tables" in metadata and table_name in metadata["tables"]:
        raise KeyError(f"Таблица '{table_name}' уже существует!")
    
    allowed_types = {"int", "str", "bool"}
    for col_name, col_type in columns:
        if col_type not in allowed_types:
            raise ValueError(f"Недопустимый тип '{col_type}' для столбца '{col_name}'. "
                            f"Допустимые типы: {', '.join(allowed_types)}")
    
    columns_with_id = [("ID", "int")] + columns
    data_dir = "data"
    data_file = f"{data_dir}/{table_name}.json"
    
    # Создаем директорию data, если её нет
    os.makedirs(data_dir, exist_ok=True)
    
    # Инициализируем файл данных пустым списком
    try:
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=2)
    except Exception as e:
        raise Exception(f"Ошибка при создании файла данных {data_file}: {e}")
    
    # Инициализируем структуру таблиц, если её нет
    if "tables" not in metadata:
        metadata["tables"] = {}
    
    # Добавляем таблицу в метаданные
    metadata["tables"][table_name] = {
        "columns": columns_with_id,
        "data_file": data_file
    }
    
    print(f"Таблица '{table_name}' успешно создана!")
    print(f"Столбцы: {[col[0] for col in columns_with_id]}")
    print(f"Файл данных: {data_file}")
    
    return metadata

@log_time
@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """
    Удаляет таблицу из метаданных.
    """
    # Проверяем существование таблицы
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise KeyError(f"Таблица '{table_name}' не существует!")
    
    # Удаляем файл с данными
    data_file = metadata["tables"][table_name]["data_file"]
    try:
        if os.path.exists(data_file):
            os.remove(data_file)
            print(f"Файл данных {data_file} удален")
    except Exception as e:
        print(f"Ошибка при удалении файла данных {data_file}: {e}")
    
    # Удаляем таблицу из метаданных
    del metadata["tables"][table_name]
    
    # Если это была последняя таблица, удаляем весь раздел tables
    if not metadata["tables"]:
        del metadata["tables"]
    
    print(f"Таблица '{table_name}' успешно удалена!")
    return metadata


@log_time
@handle_db_errors
def load_table_data(table_name, metadata):
    """
    Загружает данные таблицы из файла.
    """
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise KeyError(f"Таблица '{table_name}' не существует!")
    
    data_file = metadata["tables"][table_name]["data_file"]
    
    # Проверяем существование файла
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Файл данных {data_file} не существует для таблицы '{table_name}'")
    
    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {data_file}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке файла {data_file}: {e}")
        return []

@log_time
@handle_db_errors
def save_table_data(table_name, data, metadata):
    """
    Сохраняет данные таблицы в файл.
    """
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise KeyError(f"Таблица '{table_name}' не существует!")
    
    data_file = metadata["tables"][table_name]["data_file"]
    
    try:
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла данных {data_file}: {e}")
