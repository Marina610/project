import requests
import config


class ApiClient:
    """Обёртка над requests.Session — держим сессию живой между запросами"""

    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.API_BASE_URL
        self.session.headers.update({"Content-Type": "application/json"})

    def post(self, endpoint: str, payload: dict, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=payload, **kwargs)

    def get(self, endpoint: str, params: dict = None, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params, **kwargs)

    def set_auth_token(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})
