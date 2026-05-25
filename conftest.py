### Fixtures for the test suite
import pytest
import subprocess
from playwright.sync_api import sync_playwright, Page
from conftest import credentials


admin = credentials["username"]
password = credentials["password"]


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


@pyttest.fixture(scope="session", autouse=True)
def setup_test_environment(page: Page):
    """Set up the test environment before running tests."""

    # Requisites:
    # Tener un entorno de pruebas con wordpress, con woocommerce y el plugin a comprobar instalado
    # Tener el entorno de pruebas levantado, esto se hace usando al app de Localsite


    BASE_URL = "http://test-plugin.local"

    #Loguearse en el admin de wordpress para revisar esto
    # Ir a http://test-plugin.local/wp-admin, sino estoy logueado rellenar el formulario de login con las credenciales del admin
    page.goto(f"{BASE_URL}/wp-admin")
    username_field = page.get_by_label("username")
    password_field = page.get_by_label("password")    
    username_field.fill(admin)
    password_field.fill(password)

    # Hacer click en el botón de login
    login_button = page.get_by_role(role="button", name="Log in")
    login_button.click()

    # Acceder al menu de plugins
    page.wait_for_selector("#wpadminbar")
    page.goto(f"{BASE_URL}/wp-admin/plugins.php")

    # Revisar que tanto WooCommerce como el plugin a comprobar esten activados con otra funcion
    #TODO: woo_activate = page.locator("tr[data-slug='woocommerce'] .activate")
    #TODO: plugin_activate = page.locator(f"tr[data-slug='{plugin}'] .activate")
    # Desactivar los demas plugin
    #usar cli de wp para esto, esto se hace a mano por ahora, pero se puede automatizar con el cli de wp, esto se hace para evitar que otros plugins interfieran con las pruebas


    #Revisar que WooCommerce tiene la ultima version (esto por ahora se obvia, esto se hace manualmente)

    #Revisar que nuestro plugin(el que sea) tiene la ultim version(esto se obvia, por ahora se hace a mano)


    print("Test environment completed")

    yield
    print("Tearing down test environment...")
    # Aquí puedes agregar cualquier limpieza que necesites después de ejecutar los tests