### Fixtures for the test suite
import pytest
import subprocess
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """Set up the Playwright browser for testing."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def page(browser):
    """Set up a new page for each test."""
    page = browser.new_page()
    yield page
    page.close()