from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Базовий клас для всіх сторінок.
    Містить загальні методи, які використовуються на різних сторінках.
    """
    def __init__(self, driver: WebDriver, url: str = ""):
        self.driver = driver
        if url:
            self.driver.get(url)

    def find_element(self, locator: tuple, timeout: int = 10):
        """
        Знаходить один елемент на сторінці.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator: tuple, timeout: int = 10):
        """
        Знаходить всі елементи на сторінці, що відповідають локатору.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator: tuple, timeout: int = 10):
        """
        Клікає на елемент.
        """
        self.find_element(locator, timeout).click()

    def type_text(self, locator: tuple, text: str, timeout: int = 10):
        """
        Вводить текст в поле.
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple, timeout: int = 10) -> str:
        """
        Отримує текст елемента.
        """
        return self.find_element(locator, timeout).text

    def get_title(self) -> str:
        """
        Отримує заголовок поточної сторінки.
        """
        return self.driver.title

    def is_element_displayed(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Перевіряє, чи відображається елемент на сторінці.
        """
        try:
            return self.find_element(locator, timeout).is_displayed()
        except:
            return False