import os
import re
from collections import Counter

# Шлях до файлу з текстом (не залежить від того, звідки запущено програму)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEXT_PATH = os.path.join(BASE_DIR, 'data', 'neoterra_text.txt')


def _require_str(value, name="text"):
    """Перевіряє, що аргумент є рядком, інакше викликає TypeError."""
    if not isinstance(value, str):
        raise TypeError(f"Параметр '{name}' має бути рядком, отримано {type(value).__name__}")


# === Функції для базових операцій з рядками ===

def find_substring(text, substring):
    """
    Пошук підрядка в тексті.
    Повертає індекс першого входження або -1, якщо підрядок не знайдено.
    """
    _require_str(text, "text")
    _require_str(substring, "substring")
    return text.find(substring)


def replace_substring(text, old, new):
    """
    Заміна підрядка в тексті.
    """
    _require_str(text, "text")
    _require_str(old, "old")
    _require_str(new, "new")
    return text.replace(old, new)


def split_text(text, delimiter=' '):
    """
    Розділення тексту за роздільником.
    """
    _require_str(text, "text")
    _require_str(delimiter, "delimiter")
    if delimiter == '':
        raise ValueError("Роздільник не може бути порожнім рядком")
    return text.split(delimiter)


def _check_person(name, age):
    _require_str(name, "name")
    if isinstance(age, bool) or not isinstance(age, int):
        raise TypeError("Параметр 'age' має бути цілим числом")
    if age < 0:
        raise ValueError("Вік не може бути від'ємним")


def format_string_f(name, age):
    """
    Форматування рядка з використанням f-string.
    Приклад: "Мене звати [name] і мені [age] років."
    """
    _check_person(name, age)
    return f"Мене звати {name} і мені {age} років."


def format_string_method(name, age):
    """
    Форматування рядка з використанням методу .format().
    Приклад: "Мене звати [name] і мені [age] років."
    """
    _check_person(name, age)
    return "Мене звати {} і мені {} років.".format(name, age)


# === Функції для роботи з регулярними виразами ===

EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
PHONE_PATTERN = r'^\+380\d{9}$'
HASHTAG_PATTERN = r'#\w+'
MENTION_PATTERN = r'@\w+'
URL_PATTERN = r'https?://[^\s]+'


def extract_emails(text):
    """
    Витяг email адрес з тексту.
    """
    _require_str(text)
    return re.findall(EMAIL_PATTERN, text)


def validate_phone_number(number):
    """
    Валідація українського телефонного номера.
    Формат: +380xxxxxxxxx
    Для не-рядкових значень повертає False.
    """
    if not isinstance(number, str):
        return False
    return re.match(PHONE_PATTERN, number.strip()) is not None


def extract_hashtags(text):
    """
    Витяг хештегів з тексту.
    """
    _require_str(text)
    return re.findall(HASHTAG_PATTERN, text)


def extract_mentions(text):
    """
    Витяг згадувань користувачів з тексту (напр. @user).
    """
    _require_str(text)
    return re.findall(MENTION_PATTERN, text)


def extract_urls(text):
    """
    Витяг URL-адрес з тексту.
    """
    _require_str(text)
    return [u.rstrip('.,;:!?') for u in re.findall(URL_PATTERN, text)]


# === Функції для аналізу тексту ===

# слово: літери/цифри, можливо з дефісом, апострофом чи крапкою всередині
WORD_PATTERN = r"\w+(?:[-'’.]\w+)*"


def count_words(text):
    """
    Підрахунок кількості слів у тексті.
    """
    _require_str(text)
    return len(re.findall(WORD_PATTERN, text))


def count_sentences(text):
    """
    Підрахунок кількості речень у тексті.
    Кінець речення — це . ! або ?, після яких іде пробіл чи кінець тексту
    (тому крапки в "0.01%" чи "v5.3" не рахуються).
    """
    _require_str(text)
    return len(re.findall(r'[.!?]+\s', text + ' '))


def word_frequency(text):
    """
    Підрахунок частоти слів у тексті.
    Повертає об'єкт Counter.
    """
    _require_str(text)
    return Counter(re.findall(WORD_PATTERN, text.lower()))


def analyze_text(text):
    """
    Комплексний аналіз тексту.
    Повертає словник з результатами аналізу.
    """
    _require_str(text)
    freq = word_frequency(text)
    return {
        'word_count': count_words(text),
        'sentence_count': count_sentences(text),
        'unique_words': len(freq),
        'word_frequency': freq.most_common(10),
        'emails': extract_emails(text),
        'hashtags': extract_hashtags(text),
        'mentions': extract_mentions(text),
        'urls': extract_urls(text),
    }


def format_analysis_results(results):
    """
    Форматування результатів аналізу для зручного виведення.
    """
    if not isinstance(results, dict):
        raise TypeError("Результати аналізу мають бути словником")
    output = "Результати аналізу тексту:\n"
    output += f"  Кількість слів: {results.get('word_count', 0)}\n"
    output += f"  Кількість речень: {results.get('sentence_count', 0)}\n"
    output += f"  Унікальних слів: {results.get('unique_words', 0)}\n"
    output += "  Топ-10 найчастіших слів:\n"
    for i, (word, cnt) in enumerate(results.get('word_frequency', []), start=1):
        output += "    {:>2}. {:<15} {}\n".format(i, word, cnt)
    for title, key in (("Email", 'emails'), ("Хештеги", 'hashtags'),
                       ("Згадування", 'mentions'), ("URL", 'urls')):
        items = results.get(key, [])
        output += f"  {title}: {', '.join(items) if items else '—'}\n"
    return output


# === Практичне завдання варіанту 6: аналіз коду Python ===

FUNCTION_PATTERN = r'^[ \t]*(?:async[ \t]+)?def[ \t]+([A-Za-z_]\w*)[ \t]*\('
CLASS_PATTERN = r'^[ \t]*class[ \t]+([A-Za-z_]\w*)'
# змінна: ім'я (можливо з анотацією типу) та одинарне присвоєння "=" (не "==")
VARIABLE_PATTERN = r'^[ \t]*([A-Za-z_]\w*)[ \t]*(?::[^=\n]+)?=(?!=)'
COMMENT_PATTERN = r'#.*'


def find_functions(code):
    """
    Пошук імен функцій (def / async def) у Python-коді.
    """
    _require_str(code, "code")
    return re.findall(FUNCTION_PATTERN, code, flags=re.MULTILINE)


def find_classes(code):
    """
    Пошук імен класів у Python-коді.
    """
    _require_str(code, "code")
    return re.findall(CLASS_PATTERN, code, flags=re.MULTILINE)


def find_variables(code):
    """
    Пошук імен змінних, яким присвоюється значення (унікальні, у порядку появи).
    """
    _require_str(code, "code")
    names = re.findall(VARIABLE_PATTERN, code, flags=re.MULTILINE)
    unique = []
    for name in names:
        if name not in unique:
            unique.append(name)
    return unique


def find_comments(code):
    """
    Пошук коментарів (# ...) у Python-коді.
    """
    _require_str(code, "code")
    return re.findall(COMMENT_PATTERN, code, flags=re.MULTILINE)


def analyze_code(code):
    """
    Комплексний аналіз Python-скрипта: функції, класи, змінні, коментарі.
    """
    _require_str(code, "code")
    return {
        'functions': find_functions(code),
        'classes': find_classes(code),
        'variables': find_variables(code),
        'comments': find_comments(code),
    }


def format_code_analysis(result):
    """
    Форматування результатів аналізу коду для виведення.
    """
    if not isinstance(result, dict):
        raise TypeError("Результати аналізу мають бути словником")
    titles = (('functions', 'Функції'), ('classes', 'Класи'),
              ('variables', 'Змінні'), ('comments', 'Коментарі'))
    output = "Результати аналізу коду:\n"
    for key, title in titles:
        items = result.get(key, [])
        output += f"  {title} ({len(items)}):\n"
        for item in items:
            output += f"    - {item}\n"
    return output


# === Функція для вилучення даних за варіантом ===

# Варіант 6: коди неоптахів, напр. NB-201.
# Код стоїть одразу після слова "неоптахи"; дужки () виділяють групу - саме код.
NEOPTAH_PATTERN = r'неоптахи\s+([A-Z]{2}-\d+)'


def extract_variant_data(text, variant_pattern=NEOPTAH_PATTERN):
    """
    Вилучає дані з тексту за допомогою патерну, специфічного для варіанту.
    За замовчуванням (варіант 6) - коди неоптахів.
    """
    _require_str(text)
    _require_str(variant_pattern, "variant_pattern")
    try:
        return re.findall(variant_pattern, text)
    except re.error as e:
        raise ValueError(f"Некоректний регулярний вираз: {e}")


# === Головна частина програми ===

def read_file_content(filepath):
    """
    Читає вміст файлу. У разі помилки повертає None.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Помилка: Файл не знайдено за шляхом {filepath}")
    except PermissionError:
        print(f"Помилка: Немає доступу до файлу {filepath}")
    except UnicodeDecodeError:
        print(f"Помилка: Файл {filepath} не є текстом у кодуванні UTF-8")
    except OSError as e:
        print(f"Помилка читання файлу {filepath}: {e}")
    return None


SAMPLE_CODE = '''\
# Приклад скрипта для аналізу
PI = 3.14159
counter: int = 0

class Circle:
    """Коло."""
    def __init__(self, r):
        self.r = r  # радіус

    def area(self):
        return PI * self.r ** 2

def greet(name):
    message = f"Привіт, {name}! # не коментар"
    return message  # повертаємо рядок
'''


def main():
    """
    Головна функція, що керує виконанням програми.
    """
    print("Ласкаво просимо до аналізатора тексту!")

    text_to_analyze = read_file_content(DEFAULT_TEXT_PATH)
    if not text_to_analyze:
        return  # Завершити, якщо файл не прочитано

    while True:
        try:
            print("\nОберіть опцію:")
            print("1. Аналіз тексту 'NeoTerra 3000'")
            print("2. Валідація телефонного номера")
            print("3. Вилучення даних за варіантом (варіант 6: коди неоптахів)")
            print("4. Аналіз Python-коду (функції, змінні, коментарі)")
            print("5. Вихід")
            choice = input("Ваш вибір: ").strip()

            if choice == '1':
                results = analyze_text(text_to_analyze)
                print(format_analysis_results(results))

            elif choice == '2':
                phone = input("Введіть номер телефону для валідації (+380XXXXXXXXX): ")
                if validate_phone_number(phone):
                    print("Номер телефону валідний.")
                else:
                    print("Номер телефону невалідний.")

            elif choice == '3':
                codes = extract_variant_data(text_to_analyze)
                print(f"Коди неоптахів: {codes}")

            elif choice == '4':
                path = input("Шлях до .py файлу (Enter - використати приклад): ").strip()
                if path:
                    code = read_file_content(path)
                    if code is None:
                        continue
                else:
                    code = SAMPLE_CODE
                print(format_code_analysis(analyze_code(code)))

            elif choice == '5':
                print("Дякуємо за використання аналізатора!")
                break

            else:
                print("Невірний вибір. Спробуйте ще раз.")

        except (EOFError, KeyboardInterrupt):
            print("\nВвід перервано. Завершення роботи.")
            break
        except (TypeError, ValueError) as e:
            print(f"Некоректні дані: {e}")
        except Exception as e:
            print(f"Виникла помилка: {e}")


if __name__ == '__main__':
    main()
