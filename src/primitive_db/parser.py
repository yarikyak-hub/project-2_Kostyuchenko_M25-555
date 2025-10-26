import shlex
from .decorators import handle_db_errors


@handle_db_errors
def parse_where(where_str):
    """
    Парсит строку условия WHERE в словарь.
    """
    if not where_str:
        return None
    
    parts = shlex.split(where_str)
    
    if len(parts) != 3:
        print("Ошибка: Неверный формат условия WHERE. Используйте: поле = значение")
        return None
    
    field, operator, value_str = parts
    
    if operator != '=':
        print(f"Ошибка: Неподдерживаемый оператор '{operator}'. Поддерживается только '='")
        return None
    
    value = parse_value(value_str)
    return {field: value}


@handle_db_errors
def parse_set(set_str):
    """
    Парсит строку SET в словарь.
    """
    if not set_str:
        return None
    
    result = {}
    parts = split_by_commas(set_str)
    
    for part in parts:
        sub_parts = shlex.split(part)
        
        if len(sub_parts) != 3 or sub_parts[1] != '=':
            print(f"Ошибка: Неверный формат SET части '{part}'. Используйте: поле = значение")
            return None
        
        field, _, value_str = sub_parts
        value = parse_value(value_str)
        result[field] = value
    
    return result


@handle_db_errors
def parse_value(value_str):
    """
    Парсит строковое значение в соответствующий тип.
    """
    value_str = value_str.strip()
    
    if value_str.lower() in ['true', 'false']:
        return value_str.lower() == 'true'
    
    if value_str.isdigit() or (value_str[0] == '-' and value_str[1:].isdigit()):
        return int(value_str)
    
    return value_str


@handle_db_errors
def split_by_commas(input_str):
    """
    Разбивает строку по запятым, учитывая кавычки.
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


@handle_db_errors
def parse_where_simple(where_str):
    """
    Упрощенный парсер WHERE для простых случаев.
    """
    if not where_str:
        return None
    
    if '=' not in where_str:
        print("Ошибка: Неверный формат условия WHERE. Используйте: поле = значение")
        return None
    
    field, value_str = where_str.split('=', 1)
    field = field.strip()
    value_str = value_str.strip()
    
    value = parse_value(value_str)
    return {field: value}
