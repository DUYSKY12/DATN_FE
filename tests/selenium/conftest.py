import os
from dataclasses import dataclass

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService


@dataclass
class TestConfig:
    base_url: str
    browser: str
    headless: bool
    implicit_wait_seconds: int
    token: str
    customer_phone: str
    admin_phone: str


def _env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).lower() in {"1", "true", "yes", "on"}


@pytest.fixture(scope="session")
def config() -> TestConfig:
    return TestConfig(
        base_url=os.getenv("TEST_BASE_URL", "http://localhost:5173"),
        browser=os.getenv("TEST_BROWSER", "chrome").lower(),
        headless=_env_flag("TEST_HEADLESS", "0"),
        implicit_wait_seconds=int(os.getenv("TEST_IMPLICIT_WAIT", "5")),
        token=os.getenv("TEST_USER_TOKEN", ""),
        customer_phone=os.getenv("TEST_CUSTOMER_PHONE", ""),
        admin_phone=os.getenv("TEST_ADMIN_PHONE", ""),
    )


def _build_chrome_driver(headless: bool) -> webdriver.Chrome:
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    return webdriver.Chrome(service=ChromeService(), options=options)


def _build_edge_driver(headless: bool) -> webdriver.Edge:
    options = EdgeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    return webdriver.Edge(service=EdgeService(), options=options)


@pytest.fixture()
def driver(config: TestConfig):
    if config.browser == "edge":
        web_driver = _build_edge_driver(config.headless)
    else:
        web_driver = _build_chrome_driver(config.headless)

    web_driver.implicitly_wait(config.implicit_wait_seconds)
    yield web_driver
    web_driver.quit()
