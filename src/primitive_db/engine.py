import shlex
from .utils import load_metadata, save_metadata, create_table, drop_table

def welcome():
	'''Приветствие и игровой цикл'''
	print("Первая попытка запустить проект!")
	print("***")
	print("<command> exit - выйти из программы")
	print("<command> help - справочная информация")
	# Игровой цикл
	while True:
		command = input("Введите команду: ").strip().lower()

		if command == "exit":
			print("Выход из программы. До свидания!")
			break
		elif command == "help":
			print("<command> exit - выйти из программы")
			print("<command> help - справочная информация")
		elif command == "":
			continue  # Пропускаем пустые команды
		else:
			print(f"Неизвестная команда: '{command}'")
			print("Чтобы узнать доступные команды введите help")

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
                print("Ошибка: Используйте: create_table <table_name> <column1:type1> [column2:type2 ...]")
                continue
                
            table_name = args[1]
            columns_spec = args[2:]
            
            # Парсим спецификации столбцов
            columns = []
            for col_spec in columns_spec:
                if ":" not in col_spec:
                    print(f"Ошибка: Неверный формат столбца '{col_spec}'. Используйте name:type")
                    break
                col_name, col_type = col_spec.split(":", 1)
                columns.append((col_name, col_type))
            else:
                # Все столбцы успешно распарсены
                new_metadata = create_table(metadata, table_name, columns)
                if new_metadata is not None:
                    save_metadata(metadata_file, new_metadata)
                    print("Метаданные сохранены")
                    
        elif command == "drop_table":
            if len(args) != 2:
                print("Ошибка: Используйте: drop_table <table_name>")
                continue
                
            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)
            if new_metadata is not None:
                save_metadata(metadata_file, new_metadata)
                print("Метаданные сохранены")
                
        else:
            print(f"Неизвестная команда: '{command}'")
            print("Введите 'help' для справки по командам")
