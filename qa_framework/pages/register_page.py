from pages.base_page import BasePage
import config


class RegisterPage(BasePage):
    _REG_URL = config.REGISTER_URL

    _EMAIL_FIELD = ("xpath", "//input[@type='email']")
    _PASSWORD_FIELD = ("xpath", "//input[@type='password']")
    _CONFIRM_FIELD = ("xpath", "//input[@id='password-confirm']")
    _SUBMIT_BTN = ("xpath", "//button[@type='submit']")
    _ERROR_MSG = ("xpath", "//*[contains(@class, 'error') or contains(@class, 'alert-danger')]")
    _SUCCESS_MSG = ("xpath", "//*[contains(@class, 'success') or contains(@class, 'alert-success')]")

    def open(self):
        self.driver.get(self._REG_URL)

    def register(self, email: str, password: str, confirm: str = None):
        self.open()
        self.type(self._EMAIL_FIELD, email)
        self.type(self._PASSWORD_FIELD, password)
        if confirm is not None:
            self.type(self._CONFIRM_FIELD, confirm)
        self.click(self._SUBMIT_BTN)

    def is_error_shown(self) -> bool:
        return self.is_visible(self._ERROR_MSG)

    def is_success_shown(self) -> bool:
        return self.is_visible(self._SUCCESS_MSG)
