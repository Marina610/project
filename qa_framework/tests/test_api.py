import pytest
import allure
from utils.api_client import ApiClient
import config


@pytest.fixture(scope="module")
def api():
    return ApiClient()


@pytest.fixture(scope="module")
def auth_token(api):
    # получаем токен один раз на весь модуль — не дёргаем логин перед каждым тестом
    resp = api.post(config.API_LOGIN_PATH, {"email": config.VALID_EMAIL, "password": config.VALID_PASSWORD})
    assert resp.status_code == 200, f"Не смогли залогиниться для получения токена: {resp.text}"
    token = resp.json().get("token") or resp.json().get("access_token")
    api.set_auth_token(token)
    return token


# POST /api/auth/login

@allure.feature("API Auth")
class TestApiLogin:

    @allure.title("POST /api/auth/login — валидные данные")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_success(self, api):
        resp = api.post(config.API_LOGIN_PATH, {
            "email": config.VALID_EMAIL,
            "password": config.VALID_PASSWORD
        })

        assert resp.status_code == 200, f"Ожидали 200, получили {resp.status_code}: {resp.text}"
        body = resp.json()
        assert "token" in body or "access_token" in body, "В ответе нет токена"

    @allure.title("POST /api/auth/login — неверный пароль - 401")
    def test_login_wrong_password(self, api):
        resp = api.post(config.API_LOGIN_PATH, {
            "email": config.VALID_EMAIL,
            "password": "completely_wrong"
        })

        assert resp.status_code in (400, 401), (
            f"Ожидали 400/401 при неверном пароле, получили {resp.status_code}"
        )

    @allure.title("POST /api/auth/login — несуществующий юзер - 404 или 401")
    def test_login_unknown_user(self, api):
        resp = api.post(config.API_LOGIN_PATH, {
            "email": "go_user_go@noemail.com",
            "password": "whatever"
        })

        assert resp.status_code in (400, 401, 404), (
            f"Неожиданный статус для несуществующего юзера: {resp.status_code}"
        )

    @allure.title("POST /api/auth/login — пустое тело → 400/422")
    def test_login_empty_body(self, api):
        resp = api.post(config.API_LOGIN_PATH, {})

        assert resp.status_code in (400, 422), (
            f"Пустое тело должно вернуть ошибку валидации, а не {resp.status_code}"
        )

    @allure.title("POST /api/auth/login — только email, без пароля")
    def test_login_missing_password(self, api):
        resp = api.post(config.API_LOGIN_PATH, {"email": config.VALID_EMAIL})

        assert resp.status_code in (400, 422), f"Должна быть ошибка: {resp.status_code}"

    @allure.title("POST /api/auth/login — content-type и структура ответа")
    def test_login_response_structure(self, api):
        resp = api.post(config.API_LOGIN_PATH, {
            "email": config.VALID_EMAIL,
            "password": config.VALID_PASSWORD
        })

        assert resp.status_code == 200
        assert "application/json" in resp.headers.get("Content-Type", ""), (
            "Ответ должен быть в JSON"
        )


#  GET /api/profile/get

@allure.feature("API Auth")
class TestApiGetUser:

    @allure.title("GET /api/profile/get — авторизованный запрос")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_current_user(self, api, auth_token):
        resp = api.get(config.API_PROFILE_PATH)

        assert resp.status_code == 200, f"Ожидали 200, получили {resp.status_code}: {resp.text}"
        body = resp.json()
        # хоть что-то про юзера должно вернуться
        assert "email" in body or "id" in body or "user" in body, (
            f"Ответ не содержит данных о пользователе: {body}"
        )

    @allure.title("GET /api/profile/get — без токена - 401")
    def test_get_current_user_unauthorized(self, api):
        # временно убираем токен
        client = ApiClient()
        resp = client.get(config.API_PROFILE_PATH)

        assert resp.status_code == 401, (
            f"Без токена должен быть 401, а не {resp.status_code}"
        )