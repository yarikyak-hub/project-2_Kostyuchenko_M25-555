import time


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок в функциях базы данных.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: Обращение к несуществующему ключу - {e}")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except FileNotFoundError as e:
            print(f"Файл не найден: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка в функции {func.__name__}: {e}")
            return None
    return wrapper


def confirm_action(action_name):
    """
    Декоратор для подтверждения опасных операций.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            table_name = None
            if len(args) > 1:
                if func.__name__ == "drop_table" and len(args) > 1:
                    table_name = args[1]
            
            if table_name:
                message = f'Вы уверены, что хотите выполнить "{action_name}" таблицы "{table_name}"? [y/n]: '
            else:
                message = f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            
            response = input(message).strip().lower()
            
            if response != 'y':
                print("Операция отменена.")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    """
    Декоратор для замера времени выполнения функции.
    """
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        
        print(f"Функция {func.__name__} выполнилась за {execution_time:.3f} секунд.")
        return result
    return wrapper
