from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import config


class BasePage:

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    def find(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: tuple, text: str):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def is_visible(self, locator: tuple) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text

    def wait_for_url_to_be(self, url: str, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))

    def take_screenshot(self, name: str = "screenshot"):
        self.driver.save_screenshot(f"{name}.png")