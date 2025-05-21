from selenium.webdriver.common.by import By
from .base_page import BasePage

class SearchPage(BasePage):
    """
    Клас для взаємодії з головною сторінкою пошуку Google.
    """
    SEARCH_INPUT = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK") # Може відрізнятися залежно від мови/регіону
    LUCKY_BUTTON = (By.NAME, "btnI")  # Може відрізнятися
    IMAGES_LINK = (By.LINK_TEXT, "Зображення") # Або "Images"
    NEWS_LINK = (By.LINK_TEXT, "Новини") # Або "News"
    GOOGLE_LOGO = (By.XPATH, "//img[@alt='Google']") # XPath може бути більш стабільним


    def __init__(self, driver):
        super().__init__(driver, "https://www.google.com")

    def enter_search_query(self, query: str):
        """
        Вводить пошуковий запит.
        """
        self.type_text(self.SEARCH_INPUT, query)

    def click_search_button(self):
        """
        Клікає на кнопку "Пошук Google".
        Потрібно враховувати, що кнопка може бути не інтерактивною одразу,
        тому краще клікати на одну з двох кнопок, яка видима.
        """
        try:
            # Шукаємо кнопку в центрі сторінки (зазвичай перша)
            elements = self.driver.find_elements(*self.SEARCH_BUTTON)
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    return
        except Exception as e:
            print(f"Помилка при кліку на кнопку пошуку: {e}")
            # Альтернативний клік, якщо стандартна кнопка не спрацювала
            # Це може бути пов'язано з тим, що кнопка знаходиться у випадаючому списку підказок
            search_field = self.find_element(self.SEARCH_INPUT)
            search_field.submit() # Імітуємо натискання Enter

    def click_lucky_button(self):
        """
        Клікає на кнопку "Мені пощастить".
        """
        elements = self.driver.find_elements(*self.LUCKY_BUTTON)
        for element in elements:
            if element.is_displayed() and element.is_enabled():
                element.click()
                return

    def get_search_input_value(self) -> str:
        """
        Отримує поточне значення поля пошуку.
        """
        return self.find_element(self.SEARCH_INPUT).get_attribute("value")

    def are_search_elements_visible(self) -> bool:
        """
        Перевіряє видимість основних елементів пошуку.
        """
        return self.is_element_displayed(self.SEARCH_INPUT) and \
               self.is_element_displayed(self.SEARCH_BUTTON)

    def click_images_link(self):
        """
        Клікає на посилання "Зображення".
        """
        self.click(self.IMAGES_LINK)

    def click_news_link(self):
        """
        Клікає на посилання "Новини".
        """
        self.click(self.NEWS_LINK)

    def click_google_logo(self):
        """
        Клікає на логотип Google.
        """
        self.click(self.GOOGLE_LOGO)