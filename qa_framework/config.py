import os
from dotenv import load_dotenv

load_dotenv()

UI_BASE_URL = os.getenv("UI_BASE_URL", "http://2.59.41.2:6700")
API_BASE_URL = os.getenv("API_BASE_URL", "http://2.59.41.2:7320")

UI_LOGIN_PATH = os.getenv("UI_LOGIN_PATH", "/auth/login")
UI_REGISTER_PATH = os.getenv("UI_REGISTER_PATH", "/auth/register")

API_LOGIN_PATH = os.getenv("API_LOGIN_PATH", "/api/auth/login")
API_PROFILE_PATH = os.getenv("API_PROFILE_PATH", "/api/profile/get")

LOGIN_URL = f"{UI_BASE_URL}{UI_LOGIN_PATH}"
REGISTER_URL = f"{UI_BASE_URL}{UI_REGISTER_PATH}"

VALID_EMAIL = os.getenv("VALID_EMAIL")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")

REG_EMAIL = os.getenv("REG_EMAIL")
REG_PASSWORD = os.getenv("REG_PASSWORD")

# Настройки браузера
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
EXPLICIT_WAIT = 10
