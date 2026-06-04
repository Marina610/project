import pytest
import allure
from pages.login_page import LoginPage
import config


@allure.feature("Authorization")
@pytest.mark.usefixtures("driver")
class TestLogin:

    def setup_method(self):
        # переинициализируем page object перед каждым тестом
        self.login_page = LoginPage(self.driver)

    @allure.title("Успешная авторизация с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_valid_credentials(self):
        self.login_page.login(config.VALID_EMAIL, config.VALID_PASSWORD)

        current_url = self.login_page.get_current_url()
        assert "login" not in current_url, (
            f"После логина должен быть редирект, но всё ещё на {current_url}"
        )

    @allure.title("Авторизация с неверным паролем — ожидаем ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_wrong_password(self):
        self.login_page.login(config.VALID_EMAIL, "wrong_password_123")

        assert self.login_page.is_error_shown(), "Должно быть сообщение об ошибке при неверном пароле"

    @allure.title("Авторизация с незарегистрированным email")
    @pytest.mark.regression
    def test_login_unknown_email(self):
        self.login_page.login("notexist_xyz@test.com", config.VALID_PASSWORD)

        assert self.login_page.is_error_shown(), "Должна быть ошибка для несуществующего юзера"

    @allure.title("Попытка войти с пустым email")
    @pytest.mark.regression
    def test_login_empty_email(self):
        self.login_page.open()
        self.login_page.enter_password(config.VALID_PASSWORD)
        self.login_page.submit()

        # либо ошибка валидации, либо остались на странице логина
        current_url = self.login_page.get_current_url()
        assert "login" in current_url or self.login_page.is_error_shown(), (
            "При пустом email форма не должна отправляться"
        )

    @allure.title("Попытка войти с пустым паролем")
    @pytest.mark.regression
    def test_login_empty_password(self):
        self.login_page.open()
        self.login_page.enter_login(config.VALID_EMAIL)
        self.login_page.submit()

        current_url = self.login_page.get_current_url()
        assert "login" in current_url or self.login_page.is_error_shown(), (
            "При пустом пароле форма не должна отправляться"
        )

    @allure.title("Проверяем что страница логина открывается")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_page_opens(self):
        self.login_page.open()

        assert "login" in self.login_page.get_current_url(), "Страница логина не открылась"

    @allure.title("Email с невалидным форматом")
    def test_login_invalid_email_format(self):
        self.login_page.login("not-an-email", config.VALID_PASSWORD)

        current_url = self.login_page.get_current_url()
        assert "login" in current_url or self.login_page.is_error_shown(), (
            "Невалидный email не должен проходить"
        )
