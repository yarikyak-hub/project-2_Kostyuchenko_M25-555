from .decorators import handle_db_errors, confirm_action, log_time
from .cache import create_cacher

# Создаем кэшер для операций select
select_cache = create_cacher()


@handle_db_errors
def validate_value(value, expected_type):
    """
    Валидирует значение по ожидаемому типу.
    """
    if expected_type == "int":
        return isinstance(value, int) or (isinstance(value, str) and value.isdigit())
    elif expected_type == "str":
        return isinstance(value, str)
    elif expected_type == "bool":
        return isinstance(value, bool) or value in ["true", "false", "1", "0", True, False]
    return False


@handle_db_errors
def convert_value(value, expected_type):
    """
    Конвертирует значение в ожидаемый тип.
    """
    if expected_type == "int":
        return int(value)
    elif expected_type == "str":
        return str(value)
    elif expected_type == "bool":
        if isinstance(value, bool):
            return value
        elif str(value).lower() in ["true", "1"]:
            return True
        else:
            return False
    return value


@log_time
@handle_db_errors
def insert(metadata, table_name, values):
    """
    Вставляет новую запись в таблицу.
    """
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise KeyError(f"Таблица '{table_name}' не существует!")
    
    table_info = metadata["tables"][table_name]
    columns = table_info["columns"]
    
    expected_count = len(columns) - 1
    if len(values) != expected_count:
        raise ValueError(f"Ожидалось {expected_count} значений, получено {len(values)}")
    
    # Загружаем текущие данные таблицы
    from .utils import load_table_data, save_table_data
    table_data = load_table_data(table_name, metadata)
    
    # Генерируем новый ID
    if table_data:
        max_id = max(record.get("ID", 0) for record in table_data)
        new_id = max_id + 1
    else:
        new_id = 1
    
    # Создаем новую запись
    new_record = {"ID": new_id}
    
    # Валидируем и добавляем значения
    for i, (col_name, col_type) in enumerate(columns[1:]):  # Пропускаем ID
        value = values[i]
        
        # Валидация типа
        if not validate_value(value, col_type):
            raise ValueError(f"Неверный тип для столбца '{col_name}'. Ожидается {col_type}")
        
        # Конвертируем значение
        new_record[col_name] = convert_value(value, col_type)
    
    # Добавляем запись в данные
    table_data.append(new_record)
    
    # Сохраняем данные
    if save_table_data(table_name, table_data, metadata):
        print(f"Запись успешно добавлена в таблицу '{table_name}' с ID={new_id}")
        return table_data
    else:
        raise Exception("Ошибка при сохранении данных")

def _select_uncached(table_data, where_clause=None):
    """
    Внутренняя функция SELECT без кэширования.
    """
    if where_clause is None:
        return table_data
    
    filtered_data = []
    for record in table_data:
        match = True
        for field, value in where_clause.items():
            if field not in record or record[field] != value:
                match = False
                break
        if match:
            filtered_data.append(record)
    
    return filtered_data


@log_time
@handle_db_errors
def select(table_data, where_clause=None):
    """
    Выбирает записи из данных таблицы с кэшированием.
    """
    cache_key = _create_cache_key(table_data, where_clause)
    result = select_cache(cache_key, lambda: _select_uncached(table_data, where_clause))
    return result


def _create_cache_key(table_data, where_clause):
    """
    Создает ключ для кэша на основе данных и условий WHERE.
    """
    data_hash = hash(tuple(sorted(str(item) for item in table_data)))
    
    if where_clause:
        where_hash = hash(tuple(sorted((k, str(v)) for k, v in where_clause.items())))
    else:
        where_hash = hash("all")
    
    cache_key = f"select_{data_hash}_{where_hash}"
    return cache_key


@log_time
@handle_db_errors
def update(table_data, set_clause, where_clause):
    """
    Обновляет записи в данных таблицы.
    """
    updated_count = 0
    
    for record in table_data:
        match = True
        for field, value in where_clause.items():
            if field not in record or record[field] != value:
                match = False
                break
        
        if match:
            for field, new_value in set_clause.items():
                if field in record and field != "ID":
                    record[field] = new_value
            updated_count += 1
    
    print(f"Обновлено записей: {updated_count}")
    return table_data


@log_time
@confirm_action("удаление записей")
@handle_db_errors
def delete(table_data, where_clause):
    """
    Удаляет записи из данных таблицы.
    """
    filtered_data = []
    deleted_count = 0
    
    for record in table_data:
        match = True
        for field, value in where_clause.items():
            if field not in record or record[field] != value:
                match = False
                break
        
        if match:
            deleted_count += 1
        else:
            filtered_data.append(record)
    
    print(f"Удалено записей: {deleted_count}")
    return filtered_data


def clear_select_cache():
    """
    Очищает кэш операций SELECT.
    """
    select_cache.clear()


def get_select_cache_stats():
    """
    Возвращает статистику кэша SELECT.
    """
    return select_cache.stats()
