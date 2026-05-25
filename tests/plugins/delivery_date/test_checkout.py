from playwright.sync_api import Page, expect
import random
import os

BASE_URL = "http://test-plugin.local/"

product_url = "http://test-plugin.local/product/basic-t-shirt/"

def add_product_to_cart(page: Page):
    
    print(f"Testing checkout for product: {product_url}")

    # Ir al producto
    page.goto(product_url)

    # Añadir al carrito
    add_to_cart_button = page.locator("button.single_add_to_cart_button")

    add_to_cart_button.click()

    # Ir al carrito
    page.goto(BASE_URL + "cart")
    
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector(".cart_item", timeout=5000)  # esperar a que aparezca el producto

    # Captura opcional
    page.screenshot(path="../assets/img/cart_page.png", full_page=True)



def test_checkout(page: Page):
    '''Test the checkout process, including the delivery date selector.'''

    add_product_to_cart(page)

    page.goto(BASE_URL + "checkout") 

    page.fill("#billing_first_name", "John") 
    page.fill("#billing_last_name", "Doe") 
    page.select_option("#billing_country", "ES") 
    page.fill("#billing_address_1", "calle test") 
    page.fill("#billing_city", "Barcelona") 
    page.fill("#billing_postcode", "12345") 
    page.fill("#billing_phone", "333333333") 
    page.fill("#billing_email", "dev.doe@example.com") 

    # verificar que el envio a otra direccion esta desactivado
    shipping_checkbox = page.locator("#ship-to-different-address-checkbox")
    if shipping_checkbox.is_checked():
        shipping_checkbox.uncheck() 

    page.get_by_label("Delivery date").click()

    ## verificar que aparece el calendario de seleccion de fecha
    page.wait_for_selector("#ui-datepicker-div", timeout=5000) 

    expect(page.locator("#ui-datepicker-div")).to_be_visible() 

    page.screenshot(path="../assets/img/checkout_with_calendar.png", full_page=True) 


def test_product_messages(page: Page):
    '''Test that the product messages are displayed correctly on the product page.'''

    # Ir a la pagina de un producto
    # Revisar que ambos mensajes se muestran correctamente en la página de producto

    page.goto(product_url)
    page.wait_for_load_state("domcontentloaded")

    picked_up_message = page.locator("#ywcdd_info_shipping_date")
    expect(picked_up_message).to_be_visible()

    delivery_message = page.locator("#ywcdd_info_first_delivery_date")
    expect(delivery_message).to_be_visible()



