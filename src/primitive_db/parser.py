import shlex


def parse_where(where_str):
    """
    Парсит строку условия WHERE в словарь.
    
    Args:
        where_str (str): Строка условия, например "age = 28" или "name = 'John'"
        
    Returns:
        dict: Словарь с условиями {поле: значение} или None в случае ошибки
    """
    if not where_str:
        return None
    
    try:
        # Разбиваем строку на части
        parts = shlex.split(where_str)
        
        # Ожидаем формат: поле оператор значение
        if len(parts) != 3:
            print("Ошибка: Неверный формат условия WHERE. Используйте: поле = значение")
            return None
        
        field, operator, value_str = parts
        
        # Пока поддерживаем только оператор '='
        if operator != '=':
            print(f"Ошибка: Неподдерживаемый оператор '{operator}'. Поддерживается только '='")
            return None
        
        # Определяем тип значения и конвертируем
        value = parse_value(value_str)
        
        return {field: value}
    
    except Exception as e:
        print(f"Ошибка парсинга условия WHERE: {e}")
        return None


def parse_set(set_str):
    """
    Парсит строку SET в словарь.
    
    Args:
        set_str (str): Строка SET, например "age = 30, name = 'John'"
        
    Returns:
        dict: Словарь с полями для обновления {поле: значение} или None в случае ошибки
    """
    if not set_str:
        return None
    
    try:
        result = {}
        
        # Разбиваем по запятым, но учитываем кавычки
        parts = split_by_commas(set_str)
        
        for part in parts:
            # Разбиваем каждую часть на поле и значение
            sub_parts = shlex.split(part)
            
            if len(sub_parts) != 3 or sub_parts[1] != '=':
                print(f"Ошибка: Неверный формат SET части '{part}'. Используйте: поле = значение")
                return None
            
            field, _, value_str = sub_parts
            value = parse_value(value_str)
            
            result[field] = value
        
        return result
    
    except Exception as e:
        print(f"Ошибка парсинга SET: {e}")
        return None


def parse_value(value_str):
    """
    Парсит строковое значение в соответствующий тип.
    
    Args:
        value_str (str): Строковое значение
        
    Returns:
        Значение соответствующего типа (int, str, bool)
    """
    # Удаляем возможные пробелы
    value_str = value_str.strip()
    
    # Булевы значения
    if value_str.lower() in ['true', 'false']:
        return value_str.lower() == 'true'
    
    # Числа
    if value_str.isdigit() or (value_str[0] == '-' and value_str[1:].isdigit()):
        return int(value_str)
    
    # Строки (уже должны быть в кавычках, но shlex их уберет)
    return value_str


def split_by_commas(input_str):
    """
    Разбивает строку по запятым, учитывая кавычки.
    
    Args:
        input_str (str): Входная строка
        
    Returns:
        list: Список частей
    """
    parts = []
    current_part = []
    in_quotes = False
    quote_char = None
    
    for char in input_str:
        if char in ['"', "'"]:
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
                quote_char = None
            current_part.append(char)
        elif char == ',' and not in_quotes:
            parts.append(''.join(current_part).strip())
            current_part = []
        else:
            current_part.append(char)
    
    if current_part:
        parts.append(''.join(current_part).strip())
    
    return parts


# Альтернативная упрощенная версия для небольших случаев
def parse_where_simple(where_str):
    """
    Упрощенный парсер WHERE для простых случаев.
    
    Args:
        where_str (str): Строка условия
        
    Returns:
        dict: Словарь с условиями
    """
    if not where_str:
        return None
    
    try:
        # Простой разбор: разбиваем по '='
        if '=' not in where_str:
            print("Ошибка: Неверный формат условия WHERE. Используйте: поле = значение")
            return None
        
        field, value_str = where_str.split('=', 1)
        field = field.strip()
        value_str = value_str.strip()
        
        value = parse_value(value_str)
        
        return {field: value}
    
    except Exception as e:
        print(f"Ошибка парсинга условия WHERE: {e}")
        return None
