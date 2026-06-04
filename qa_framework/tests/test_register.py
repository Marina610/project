import pytest
import allure
from pages.register_page import RegisterPage
import config


@allure.feature("Registration")
@pytest.mark.usefixtures("driver")
class TestRegister:

    def setup_method(self):
        self.reg_page = RegisterPage(self.driver)

    @allure.title("Регистрация с уже существующим email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_register_existing_email(self):
        # уже зарегистрированный — должна быть ошибка
        self.reg_page.register(config.VALID_EMAIL, config.VALID_PASSWORD, config.VALID_PASSWORD)

        assert self.reg_page.is_error_shown(), "Ожидали ошибку при регистрации с существующим email"

    @allure.title("Регистрация с пустым email")
    @pytest.mark.regression
    def test_register_empty_email(self):
        self.reg_page.open()
        self.reg_page.type(self.reg_page._PASSWORD_FIELD, config.REG_PASSWORD)
        self.reg_page.click(self.reg_page._SUBMIT_BTN)

        current_url = self.reg_page.get_current_url()
        assert "register" in current_url or self.reg_page.is_error_shown()

    @allure.title("Пароль и подтверждение не совпадают")
    @pytest.mark.regression
    def test_register_password_mismatch(self):
        self.reg_page.register(config.REG_EMAIL, "Pass1234!", "DifferentPass!")

        assert self.reg_page.is_error_shown(), "Должна быть ошибка при несовпадении паролей"

    @allure.title("Слишком короткий пароль")
    @pytest.mark.regression
    def test_register_short_password(self):
        self.reg_page.register(config.REG_EMAIL, "123", "123")

        assert self.reg_page.is_error_shown(), "Ожидали ошибку валидации короткого пароля"
