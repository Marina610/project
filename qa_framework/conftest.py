import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
import config


@pytest.fixture(autouse=False)
def driver(request):
    options = Options()

    if config.HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # убираем баннер "Chrome is being controlled by automated software"
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    request.cls.driver = driver
    yield driver

    driver.quit()

@pytest.fixture
def logged_in_driver(driver, request):
    """Драйвер с уже выполненным логином"""
    login_page = LoginPage(driver)
    login_page.login(config.VALID_EMAIL, config.VALID_PASSWORD)
    yield driver
