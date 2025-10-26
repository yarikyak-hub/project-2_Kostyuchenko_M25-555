def create_cacher():
    cache = {}
    
    def cache_result(key, value_func):
        if key in cache:
            # print(f"Кэш попадание для ключа: {key}")  # Для отладки
            return cache[key]
        else:
            # print(f"Кэш промах для ключа: {key}")  # Для отладки
            result = value_func()
            cache[key] = result
            return result
    
    def clear_cache():
        """Очищает весь кэш"""
        cache.clear()
        print("Кэш очищен")
    
    def get_cache_stats():
        """Возвращает статистику кэша"""
        return {
            'size': len(cache),
            'keys': list(cache.keys())
        }
    
    # Добавляем методы для управления кэшом
    cache_result.clear = clear_cache
    cache_result.stats = get_cache_stats
    
    return cache_result
