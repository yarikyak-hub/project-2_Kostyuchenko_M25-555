import json
import os


def load_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {filepath}: {e}")
        return {}
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке файла {filepath}: {e}")
        return {}

def save_metadata(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}")

def create_table(metadata, table_name, columns):
# Проверяем, существует ли уже таблица
    if "tables" in metadata and table_name in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' уже существует!")
        return None
    
    # Проверяем корректность типов данных
    allowed_types = {"int", "str", "bool"}
    for col_name, col_type in columns:
        if col_type not in allowed_types:
            print(f"Ошибка: Недопустимый тип '{col_type}' для столбца '{col_name}'. "
                  f"Допустимые типы: {', '.join(allowed_types)}")
            return None
    
    # Добавляем столбец ID:int в начало
    columns_with_id = [("ID", "int")] + columns
    
    # Создаем файл для данных таблицы
    data_dir = "data"
    data_file = f"{data_dir}/{table_name}.json"
    
    # Создаем директорию data, если её нет
    os.makedirs(data_dir, exist_ok=True)
    
    # Инициализируем файл данных пустым списком
    try:
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при создании файла данных {data_file}: {e}")
        return None
    
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

def drop_table(metadata, table_name):
 # Проверяем существование таблицы
    if "tables" not in metadata or table_name not in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' не существует!")
        return None
    
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

def load_table_data(table_name, metadata):
    if "tables" not in metadata or table_name not in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' не существует!")
        return []
    
    data_file = metadata["tables"][table_name]["data_file"]
    
    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл данных {data_file} не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {data_file}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке файла {data_file}: {e}")
        return []

def save_table_data(table_name, data, metadata):
    if "tables" not in metadata or table_name not in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' не существует!")
        return False
    
    data_file = metadata["tables"][table_name]["data_file"]
    
    try:
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла данных {data_file}: {e}")
        return False
