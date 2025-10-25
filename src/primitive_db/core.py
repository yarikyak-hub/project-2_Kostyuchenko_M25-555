def validate_value(value, expected_type):
    """
    Валидирует значение по ожидаемому типу.
    
    Args:
        value: Значение для валидации
        expected_type (str): Ожидаемый тип ('int', 'str', 'bool')
        
    Returns:
        bool: True если значение соответствует типу
    """
    if expected_type == "int":
        return isinstance(value, int) or (isinstance(value, str) and value.isdigit())
    elif expected_type == "str":
        return isinstance(value, str)
    elif expected_type == "bool":
        return isinstance(value, bool) or value in ["true", "false", "1", "0", True, False]
    return False


def convert_value(value, expected_type):
    """
    Конвертирует значение в ожидаемый тип.
    
    Args:
        value: Значение для конвертации
        expected_type (str): Ожидаемый тип ('int', 'str', 'bool')
        
    Returns:
        Конвертированное значение
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


def insert(metadata, table_name, values, table_data):
    """
    Вставляет новую запись в таблицу.
    
    Args:
        metadata (dict): Метаданные базы данных
        table_name (str): Имя таблицы
        values (list): Список значений для вставки
        
    Returns:
        list: Обновленные данные таблицы или None в случае ошибки
    """
    # Проверяем существование таблицы
    if "tables" not in metadata or table_name not in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' не существует!")
        return None
    
    table_info = metadata["tables"][table_name]
    columns = table_info["columns"]
    
    # Проверяем количество значений (минус ID столбец)
    expected_count = len(columns) - 1
    if len(values) != expected_count:
        print(f"Ошибка: Ожидалось {expected_count} значений, получено {len(values)}")
        print(f"Столбцы (кроме ID): {[col[0] for col in columns[1:]]}")
        return None
    
    # Загружаем текущие данные таблицы
    
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
            print(f"Ошибка: Неверный тип для столбца '{col_name}'. Ожидается {col_type}")
            return None
        
        # Конвертируем значение
        new_record[col_name] = convert_value(value, col_type)
    
    # Добавляем запись в данные
    table_data.append(new_record)
    
    # Сохраняем данные
    from .utils import save_table_data
    if save_table_data(table_name, table_data, metadata):
        print(f"Запись успешно добавлена в таблицу '{table_name}' с ID={new_id}")
        return table_data
    else:
        print("Ошибка при сохранении данных")
        return None


def select(table_data, where_clause=None):
    """
    Выбирает записи из данных таблицы.
    
    Args:
        table_data (list): Данные таблицы
        where_clause (dict): Условие фильтрации {поле: значение}
        
    Returns:
        list: Отфильтрованные записи
    """
    if where_clause is None:
        return table_data
    
    # Фильтруем записи по условию
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


def update(table_data, set_clause, where_clause):
    """
    Обновляет записи в данных таблицы.
    
    Args:
        table_data (list): Данные таблицы
        set_clause (dict): Поля для обновления {поле: новое_значение}
        where_clause (dict): Условие фильтрации {поле: значение}
        
    Returns:
        list: Обновленные данные таблицы
    """
    updated_count = 0
    
    for record in table_data:
        # Проверяем условие WHERE
        match = True
        for field, value in where_clause.items():
            if field not in record or record[field] != value:
                match = False
                break
        
        # Если запись подходит, обновляем её
        if match:
            for field, new_value in set_clause.items():
                if field in record and field != "ID":  # Не позволяем изменять ID
                    record[field] = new_value
            updated_count += 1
    
    print(f"Обновлено записей: {updated_count}")
    return table_data


def delete(table_data, where_clause):
    """
    Удаляет записи из данных таблицы.
    
    Args:
        table_data (list): Данные таблицы
        where_clause (dict): Условие фильтрации {поле: значение}
        
    Returns:
        list: Обновленные данные таблицы
    """
    # Фильтруем записи, которые НЕ удовлетворяют условию
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
