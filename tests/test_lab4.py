import unittest
import sys
import os

# Додаємо шлях до папки src, щоб можна було імпортувати lab4
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from collections import Counter

from lab4 import (
    find_substring,
    replace_substring,
    split_text,
    format_string_f,
    format_string_method,
    extract_emails,
    validate_phone_number,
    extract_hashtags,
    extract_mentions,
    extract_urls,
    count_words,
    count_sentences,
    word_frequency,
    analyze_text,
    format_analysis_results,
    find_functions,
    find_classes,
    find_variables,
    find_comments,
    analyze_code,
    extract_variant_data,
    read_file_content,
    DEFAULT_TEXT_PATH,
)

CODE = '''\
# заголовок
PI = 3.14
count: int = 0
if count == 1:
    pass

class Shape:
    def area(self):
        return 0  # площа

async def fetch(url):
    text = "abc"
    return text
'''


class TestTextAnalyzer(unittest.TestCase):

    # --- базові операції з рядками ---
    def test_find_substring(self):
        self.assertEqual(find_substring("Hello, world!", "world"), 7)
        self.assertEqual(find_substring("Hello", "xyz"), -1)

    def test_replace_substring(self):
        self.assertEqual(replace_substring("Hello, world!", "world", "Python"), "Hello, Python!")

    def test_split_text(self):
        self.assertEqual(split_text("Hello, world!", ", "), ["Hello", "world!"])
        self.assertEqual(split_text("a b c"), ["a", "b", "c"])

    def test_split_text_empty_delimiter(self):
        with self.assertRaises(ValueError):
            split_text("abc", "")

    def test_format_string_f(self):
        self.assertEqual(format_string_f("Alice", 30), "Мене звати Alice і мені 30 років.")

    def test_format_string_method(self):
        self.assertEqual(format_string_method("Bob", 25), "Мене звати Bob і мені 25 років.")

    def test_formatters_equal(self):
        self.assertEqual(format_string_f("Ліза", 7), format_string_method("Ліза", 7))

    def test_format_invalid_input(self):
        with self.assertRaises(TypeError):
            format_string_f("Alice", "30")
        with self.assertRaises(ValueError):
            format_string_method("Alice", -1)

    def test_type_errors(self):
        for func in (find_substring, replace_substring):
            with self.assertRaises(TypeError):
                func(123, "a") if func is find_substring else func(123, "a", "b")

    # --- регулярні вирази ---
    def test_extract_emails(self):
        text = "Contact us at info@example.com or support@test.com"
        self.assertEqual(extract_emails(text), ["info@example.com", "support@test.com"])
        self.assertEqual(extract_emails("без пошти"), [])

    def test_validate_phone_number(self):
        self.assertTrue(validate_phone_number("+380123456789"))
        self.assertFalse(validate_phone_number("12345"))
        self.assertFalse(validate_phone_number("+3801234567890"))
        self.assertFalse(validate_phone_number("380123456789"))
        self.assertFalse(validate_phone_number("+3000-555-NEO-TERRA"))
        self.assertFalse(validate_phone_number(None))

    def test_extract_hashtags(self):
        self.assertEqual(extract_hashtags("I love #Python and #Programming"),
                         ["#Python", "#Programming"])

    def test_extract_mentions(self):
        self.assertEqual(extract_mentions("Hi @alice and @bob_1!"), ["@alice", "@bob_1"])

    def test_extract_urls(self):
        self.assertEqual(extract_urls("Сайт: https://example.com/a."), ["https://example.com/a"])

    # --- аналіз тексту ---
    def test_count_words(self):
        self.assertEqual(count_words("Hello, world!"), 2)
        self.assertEqual(count_words("NT-Net v5.3 працює"), 3)
        self.assertEqual(count_words(""), 0)

    def test_count_sentences(self):
        self.assertEqual(count_sentences("Привіт! Як справи? Добре."), 3)
        self.assertEqual(count_sentences("Рівень 0.01% і v5.3 - це не кінець."), 1)

    def test_word_frequency(self):
        freq = word_frequency("Так, так! Ні.")
        self.assertIsInstance(freq, Counter)
        self.assertEqual(freq["так"], 2)
        self.assertEqual(freq["ні"], 1)

    def test_analyze_text_and_format(self):
        res = analyze_text("Привіт #тест! Пиши на a@b.com")
        self.assertEqual(res['emails'], ["a@b.com"])
        self.assertEqual(res['hashtags'], ["#тест"])
        out = format_analysis_results(res)
        self.assertIn("Кількість слів", out)
        self.assertIn("a@b.com", out)

    def test_format_results_invalid(self):
        with self.assertRaises(TypeError):
            format_analysis_results("не словник")

    # --- варіант 6: аналіз коду ---
    def test_find_functions(self):
        self.assertEqual(find_functions(CODE), ["area", "fetch"])

    def test_find_classes(self):
        self.assertEqual(find_classes(CODE), ["Shape"])

    def test_find_variables(self):
        # "count == 1" не є присвоєнням; "text" - змінна всередині функції
        self.assertEqual(find_variables(CODE), ["PI", "count", "text"])

    def test_find_comments(self):
        self.assertEqual(find_comments(CODE), ["# заголовок", "# площа"])

    def test_analyze_code(self):
        res = analyze_code(CODE)
        self.assertEqual(set(res), {'functions', 'classes', 'variables', 'comments'})
        self.assertEqual(len(res['comments']), 2)

    def test_code_type_error(self):
        with self.assertRaises(TypeError):
            find_functions(None)

    # --- варіант 6: коди неоптахів ---
    def test_extract_neoptah_codes_sample(self):
        self.assertEqual(extract_variant_data("рідкісні види, як-от неоптахи NB-201."), ["NB-201"])
        self.assertEqual(extract_variant_data("неоптахи NB-7 та неоптахи ZZ-1000"),
                         ["NB-7", "ZZ-1000"])

    def test_neoptah_ignores_other_models(self):
        text = "гіперлупи HY-400, реактори FR-1000, неоптахи NB-201"
        self.assertEqual(extract_variant_data(text), ["NB-201"])

    def test_neoptah_in_real_file(self):
        text = read_file_content(DEFAULT_TEXT_PATH)
        self.assertIsNotNone(text)
        self.assertEqual(extract_variant_data(text), ["NB-201"])

    def test_bad_pattern(self):
        with self.assertRaises(ValueError):
            extract_variant_data("text", "([")

    def test_read_missing_file(self):
        self.assertIsNone(read_file_content("no/such/file.txt"))

    def test_real_file_analysis(self):
        res = analyze_text(read_file_content(DEFAULT_TEXT_PATH))
        self.assertEqual(res['emails'], ["info@neoterra3000.earth"])
        self.assertEqual(len(res['hashtags']), 4)


if __name__ == '__main__':
    # Запуск тестів
    unittest.main(verbosity=2)
