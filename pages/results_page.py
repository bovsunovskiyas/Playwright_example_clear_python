from selenium.webdriver.common.by import By
from .base_page import BasePage

class ResultsPage(BasePage):
    """
    Клас для взаємодії зі сторінкою результатів пошуку Google.
    """
    SEARCH_RESULTS_STATS = (By.ID, "result-stats") # ID елемента, що показує кількість результатів
    SEARCH_RESULT_ITEMS = (By.XPATH, "//div[@class='g']") # Загальний XPath для елементів результатів
    IMAGES_TAB_ACTIVE = (By.XPATH, "//a[contains(@aria-label, 'Зображення') and @aria-selected='true']") # "Images"
    NEWS_TAB_ACTIVE = (By.XPATH, "//a[contains(@aria-label, 'Новини') and @aria-selected='true']") # "News"
    NEXT_PAGE_LINK = (By.ID, "pnnext")
    SEARCH_INPUT_ON_RESULTS_PAGE = (By.NAME, "q") # Поле пошуку на сторінці результатів


    def __init__(self, driver):
        super().__init__(driver) # URL не передаємо, бо переходимо з іншої сторінки

    def get_search_results_stats_text(self) -> str:
        """
        Отримує текст статистики результатів пошуку.
        """
        if self.is_element_displayed(self.SEARCH_RESULTS_STATS):
            return self.get_text(self.SEARCH_RESULTS_STATS)
        return ""

    def count_search_results(self) -> int:
        """
        Повертає кількість знайдених результатів на поточній сторінці.
        """
        if self.is_element_displayed(self.SEARCH_RESULT_ITEMS, timeout=5):
            return len(self.find_elements(self.SEARCH_RESULT_ITEMS))
        return 0

    def get_first_result_title(self) -> str:
        """
        Отримує заголовок першого результату пошуку.
        """
        first_result_title = (By.XPATH, "(//div[@class='g']//h3)[1]") # XPath для заголовку першого результату
        if self.is_element_displayed(first_result_title):
            return self.get_text(first_result_title)
        return ""

    def is_images_tab_active(self) -> bool:
        """
        Перевіряє, чи активна вкладка "Зображення".
        """
        return self.is_element_displayed(self.IMAGES_TAB_ACTIVE)

    def is_news_tab_active(self) -> bool:
        """
        Перевіряє, чи активна вкладка "Новини".
        """
        return self.is_element_displayed(self.NEWS_TAB_ACTIVE)

    def click_next_page(self):
        """
        Клікає на посилання для переходу на наступну сторінку результатів.
        """
        if self.is_element_displayed(self.NEXT_PAGE_LINK):
            self.click(self.NEXT_PAGE_LINK)
            return True
        return False

    def get_search_input_value_on_results_page(self) -> str:
        """
        Отримує значення поля пошуку на сторінці результатів.
        """
        return self.find_element(self.SEARCH_INPUT_ON_RESULTS_PAGE).get_attribute("value")