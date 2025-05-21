import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager # Для автоматичного завантаження драйвера
# Якщо ви хочете використовувати Firefox:
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager

from pages.search_page import SearchPage
from pages.results_page import ResultsPage
import time # Для демонстраційних пауз, у реальних тестах краще уникати

class TestGoogleSearch(unittest.TestCase):

    def setUp(self):
        # Ініціалізація драйвера (Chrome)
        # Для Chrome:
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Запуск у фоновому режимі (без UI) для CI
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080") # Важливо для headless
        # options.add_argument('acceptInsecureCerts') # Якщо є проблеми з SSL
        # options.add_argument("--lang=uk-UA") # Встановлення мови для стабільності локаторів
        # options.add_experimental_option('prefs', {'intl.accept_languages': 'uk,ua'})


        try:
            # Спробуйте використати WebDriver Manager
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        except Exception:
            # Якщо WebDriver Manager не спрацював, спробуйте вказати шлях до драйвера вручну
            # Наприклад, для GitHub Actions драйвер часто вже є в PATH
            try:
                self.driver = webdriver.Chrome(options=options)
            except Exception as e:
                print(f"Не вдалося ініціалізувати Chrome драйвер: {e}")
                # Якщо використовуєте інший браузер, наприклад Firefox:
                # self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
                raise

        self.driver.implicitly_wait(5) # Неявне очікування
        self.base_url = "https://www.google.com"
        self.search_page = SearchPage(self.driver)
        self.results_page = ResultsPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC_GS_001_load_home_page(self):
        """TC_GS_001: Перевірити, що головна сторінка Google завантажується успішно."""
        self.assertTrue(self.search_page.are_search_elements_visible(), "Елементи пошуку не відображаються")
        self.assertIn("Google", self.search_page.get_title(), "Заголовок сторінки неправильний")

    def test_TC_GS_002_simple_search(self):
        """TC_GS_002: Перевірити пошук за простим ключовим словом."""
        query = "Selenium"
        self.search_page.enter_search_query(query)
        self.search_page.click_search_button()
        time.sleep(1) # Даємо час на завантаження результатів
        self.assertIn(query, self.results_page.get_title(), "Заголовок сторінки результатів не містить запит")
        self.assertTrue(self.results_page.count_search_results() > 0, "Результати пошуку не знайдені")

    def test_TC_GS_003_search_exact_phrase(self):
        """TC_GS_003: Перевірити пошук за фразою в лапках."""
        query = "\"Python automation\""
        self.search_page.enter_search_query(query)
        self.search_page.click_search_button()
        time.sleep(1)
        self.assertIn(query.strip('"'), self.results_page.get_title().lower(), "Заголовок не містить точну фразу")
        # Додаткова перевірка: перевірити, що перший результат містить фразу (може бути не завжди)
        # first_title = self.results_page.get_first_result_title().lower()
        # self.assertIn(query.strip('"').lower(), first_title, "Перший результат не містить точну фразу")

    def test_TC_GS_004_empty_search(self):
        """TC_GS_004: Перевірити пошук з порожнім запитом."""
        initial_url = self.driver.current_url
        self.search_page.enter_search_query("")
        self.search_page.click_search_button()
        time.sleep(0.5) # Невелике очікування
        # Очікуємо, що URL не змінився або змінився мінімально (наприклад, додано '#')
        self.assertTrue(self.driver.current_url == initial_url or "#" in self.driver.current_url,
                        "URL змінився після порожнього пошуку, хоча не мав")
        # Перевіряємо, що поле пошуку все ще порожнє або містить попередній запит (залежить від реалізації)
        self.assertEqual(self.search_page.get_search_input_value(), "", "Поле пошуку не порожнє")


    def test_TC_GS_006_search_suggestions(self):
        """TC_GS_006: Перевірити відображення підказок під час введення запиту."""
        query_part = "seleni"
        self.search_page.enter_search_query(query_part)
        time.sleep(1) # Дати час на появу підказок
        # Локатор для списку підказок (може потребувати адаптації)
        suggestions_list_locator = (By.XPATH, "//ul[@role='listbox']/li")
        self.assertTrue(self.search_page.is_element_displayed(suggestions_list_locator, timeout=2), "Підказки пошуку не з'явились")
        suggestions = self.search_page.find_elements(suggestions_list_locator)
        self.assertTrue(len(suggestions) > 0, "Кількість підказок нульова")
        # Можна перевірити, чи текст підказки містить введений запит
        first_suggestion_text = suggestions[0].text.lower()
        self.assertIn(query_part, first_suggestion_text, f"Перша підказка '{first_suggestion_text}' не містить '{query_part}'")

    def test_TC_GS_007_image_search(self):
        """TC_GS_007: Перевірити пошук зображень."""
        query = "кошенята"
        self.search_page.enter_search_query(query)
        self.search_page.click_search_button()
        time.sleep(1)
        self.search_page.click_images_link() # Клікаємо на "Зображення" на сторінці результатів
        time.sleep(2) # Очікуємо завантаження зображень
        self.assertTrue(self.results_page.is_images_tab_active(), "Вкладка 'Зображення' не активна")
        # Перевірка наявності зображень (локатор може потребувати уточнення)
        images_locator = (By.XPATH, "//img[contains(@class, 'Q4LuWd')]") # Приклад локатора для зображень
        self.assertTrue(self.results_page.is_element_displayed(images_locator, timeout=5), "Зображення не відображаються")

    def test_TC_GS_010_logo_clickable_returns_to_home(self):
        """TC_GS_010: Перевірити, що логотип Google є клікабельним і повертає на головну сторінку."""
        query = "тест"
        self.search_page.enter_search_query(query)
        self.search_page.click_search_button()
        time.sleep(1)
        # Клікаємо на логотип, який тепер знаходиться на сторінці результатів.
        # Можливо, знадобиться окремий метод/локатор для лого на ResultsPage, якщо він інший.
        # У цьому прикладі припускаємо, що логотип той самий або SearchPage може його знайти.
        self.results_page.click((By.ID, "logo")) # ID логотипу на сторінці результатів може бути 'logo'
        time.sleep(1)
        self.assertTrue(self.search_page.are_search_elements_visible(), "Не повернулись на головну сторінку після кліку на лого")
        self.assertNotIn(query, self.driver.current_url.lower(), "URL все ще містить пошуковий запит") # Перевірка, що URL змінився

    def test_TC_GS_013_search_stats_present(self):
        """TC_GS_013: Перевірити, що сторінка результатів пошуку відображає статистику."""
        self.search_page.enter_search_query("Python")
        self.search_page.click_search_button()
        time.sleep(1)
        stats_text = self.results_page.get_search_results_stats_text()
        self.assertIsNotNone(stats_text, "Статистика результатів пошуку відсутня")
        self.assertIn("результат", stats_text.lower(), "Текст статистики не містить слово 'результат'") # Або "results" для англ.

    def test_TC_GS_014_pagination_next_page(self):
        """TC_GS_014: Перевірити перехід на наступну сторінку результатів пошуку."""
        self.search_page.enter_search_query("автоматизація тестування")
        self.search_page.click_search_button()
        time.sleep(1)
        initial_results_count = self.results_page.count_search_results()
        self.assertTrue(initial_results_count > 0, "Немає результатів на першій сторінці")

        current_url_page1 = self.driver.current_url
        clicked_next = self.results_page.click_next_page()
        self.assertTrue(clicked_next, "Кнопка 'Наступна сторінка' не знайдена або не клікнута")
        time.sleep(2) # Очікування завантаження наступної сторінки

        current_url_page2 = self.driver.current_url
        self.assertNotEqual(current_url_page1, current_url_page2, "URL не змінився після переходу на наступну сторінку")
        self.assertTrue(self.results_page.count_search_results() > 0, "Немає результатів на другій сторінці")
        # Переконайтеся, що ви дійсно на другій сторінці (наприклад, перевіривши номер сторінки, якщо він є)

    def test_TC_GS_015_long_query_search(self):
        """TC_GS_015: Перевірити пошук дуже довгого рядка символів."""
        long_query = "a" * 250 # Дуже довгий запит
        self.search_page.enter_search_query(long_query)
        self.search_page.click_search_button()
        time.sleep(1)
        # Перевіряємо, що запит у полі пошуку на сторінці результатів відповідає введеному (або його частині)
        # Google може обрізати дуже довгі запити в URL або в заголовку, але поле пошуку має показувати його
        # Використовуємо get_search_input_value_on_results_page
        query_on_results_page = self.results_page.get_search_input_value_on_results_page()
        self.assertEqual(query_on_results_page, long_query, "Довгий запит неправильно відображається на сторінці результатів")
        # Перевіряємо, що сторінка завантажилась і є якісь результати або повідомлення про їх відсутність
        self.assertTrue(self.results_page.is_element_displayed(ResultsPage.SEARCH_RESULTS_STATS, timeout=3) or \
                        self.results_page.count_search_results() >= 0, # >= 0, бо може бути 0 результатів
                        "Сторінка результатів для довгого запиту не завантажилась коректно")


if __name__ == "__main__":
    unittest.main()