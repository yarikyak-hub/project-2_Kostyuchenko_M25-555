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
    
    # Инициализируем структуру таблиц, если её нет
    if "tables" not in metadata:
        metadata["tables"] = {}
    
    # Добавляем таблицу в метаданные
    metadata["tables"][table_name] = {
        "columns": columns_with_id,
        "data": []  # Будущие данные таблицы
    }
    
    print(f"Таблица '{table_name}' успешно создана!")
    print(f"Столбцы: {[col[0] for col in columns_with_id]}")
    
    return metadata

def drop_table(metadata, table_name):
    # Проверяем существование таблицы
    if "tables" not in metadata or table_name not in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' не существует!")
        return None
    
    # Удаляем таблицу из метаданных
    del metadata["tables"][table_name]
    
    # Если это была последняя таблица, удаляем весь раздел tables
    if not metadata["tables"]:
        del metadata["tables"]
    
    print(f"Таблица '{table_name}' успешно удалена!")
    return metadata
