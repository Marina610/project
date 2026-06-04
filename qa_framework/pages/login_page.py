from pages.base_page import BasePage
import config


class LoginPage(BasePage):
    # локаторы — держим всё здесь, чтобы не лазить по тестам при смене вёрстки
    _LOGIN_FIELD = ("xpath", "//input[@type='email']")
    _PASSWORD_FIELD = ("xpath", "//input[@type='password']")
    _SUBMIT_BTN = ("xpath", "//button[@type='submit']")
    _ERROR_MSG = ("xpath", "//*[contains(@class, 'error') or contains(@class, 'alert-danger')]")
    #_SUCCESS_REDIRECT = ("xpath", "//*[contains(@class, 'dashboard') or contains(@class, 'navbar-brand')]")

    def open(self):
        self.driver.get(config.LOGIN_URL)

    def enter_login(self, email: str):
        self.type(self._LOGIN_FIELD, email)

    def enter_password(self, password: str):
        self.type(self._PASSWORD_FIELD, password)

    def submit(self):
        self.click(self._SUBMIT_BTN)

    def login(self, email: str, password: str):
        # удобный метод для полного флоу логина
        self.open()
        self.enter_login(email)
        self.enter_password(password)
        self.submit()

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MSG)

    def is_error_shown(self) -> bool:
        return self.is_visible(self._ERROR_MSG)
