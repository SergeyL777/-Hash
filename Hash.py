class HashTable:
    def __init__(self, size=5):
        self.size = size
        self.count = 0
        # Используем список списков для обработки коллизий (метод цепочек)
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        """Простая хеш‑функция на основе суммы ASCII‑кодов"""
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, key, value):
        """Вставка элемента в хеш‑таблицу"""
        index = self._hash(key)
        bucket = self.table[index]

        # Проверяем, существует ли ключ — обновляем значение
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Если ключа нет — добавляем новую пару
        bucket.append((key, value))
        self.count += 1

        # Проверяем необходимость увеличения размера
        if self.count > self.size:
            self.resize()

    def search(self, key):
        """Поиск элемента по ключу"""
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Ключ '{key}' не найден")

    def delete(self, key):
        """Удаление элемента по ключу"""
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return
        raise KeyError(f"Ключ '{key}' не найден")

    def resize(self):
        """Увеличение размера таблицы вдвое и перераспределение элементов"""
        old_table = self.table
        self.size *= 2
        self.count = 0
        self.table = [[] for _ in range(self.size)]

        # Перераспределяем все элементы
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def __str__(self):
        """Строковое представление таблицы для отладки"""
        result = []
        for i, bucket in enumerate(self.table):
            if bucket:
                result.append(f"{i}: {bucket}")
        return "\n".join(result)



def string_hash(s):
    """
    Вычисляет хеш‑значение строки как сумму ASCII‑кодов всех символов.

    Args:
        s (str): входная строка

    Returns:
        int: хеш‑значение
    """
    return sum(ord(char) for char in s)



class StringHashDict:
    """
    Словарь, где ключами являются строки, а значениями — их хеш‑значения.
    Использует хеш‑таблицу для эффективного хранения и поиска.
    """
    def __init__(self):
        self.hash_table = HashTable()

    def add(self, string):
        """
        Добавляет строку в словарь и сохраняет её хеш‑значение.

        Args:
            string (str): строка для добавления
        """
        hash_value = string_hash(string)
        self.hash_table.insert(string, hash_value)

    def get(self, string):
        """
        Получает хеш‑значение для заданной строки.

        Args:
            string (str): искомая строка

        Returns:
            int: хеш‑значение строки

        Raises:
            KeyError: если строка не найдена в словаре
        """
        return self.hash_table.search(string)

    def remove(self, string):
        """
        Удаляет строку из словаря.

        Args:
            string (str): строка для удаления
        """
        self.hash_table.delete(string)



# Тестирование всей системы
print("=== ТЕСТИРОВАНИЕ HASHTABLE ===")
ht = HashTable(5)

# Добавляем 10 элементов
test_data = [
    ("apple", 1),
    ("banana", 2),
    ("cherry", 3),
    ("date", 4),
    ("elderberry", 5),
    ("fig", 6),
    ("grape", 7),
    ("honeydew", 8),
    ("kiwi", 9),
    ("lemon", 10)
]

print(f"Начальный размер таблицы: {ht.size}")
print("\nДобавляем элементы:")
for key, value in test_data:
    ht.insert(key, value)
    print(f"Вставлен: {key} -> {value}")

print(f"\nРазмер таблицы после добавления 10 элементов: {ht.size}")
print(f"Содержимое таблицы:\n{ht}")

# Проверка поиска
print("\nПроверка поиска:")
print(f"apple: {ht.search('apple')}")
print(f"lemon: {ht.search('lemon')}")

# Проверка удаления
print("\nУдаляем 'banana':")
ht.delete('banana')
try:
    print(f"banana: {ht.search('banana')}")
except KeyError as e:
    print(e)

print("\n=== ТЕСТИРОВАНИЕ STRING_HASH ===")
test_strings = ["hello", "world", "python", "hash", "test"]

for s in test_strings:
    hash_value = string_hash(s)
    print(f"'{s}' -> {hash_value}")

print("\n=== ТЕСТИРОВАНИЕ STRINGHASHDICT ===")
hash_dict = StringHashDict()

# Добавляем строки
test_words = ["cat", "dog", "bird", "fish", "turtle"]
print("Добавляем строки в словарь:")
for word in test_words:
    hash_dict.add(word)
    print(f"{word} -> {hash_dict.get(word)}")

# Поиск значений
print("\nПоиск значений:")
for word in ["cat", "dog", "unknown"]:
    try:
        print(f"{word}: {hash_dict.get(word)}")
    except KeyError as e:
        print(f"{word}: Ошибка — {e}")

# Удаление
print("\nУдаляем 'bird':")
hash_dict.remove("bird")
try:
    print(f"bird: {hash_dict.get('bird')}")
except KeyError as e:
    print(f"bird: Ошибка — {e}")
