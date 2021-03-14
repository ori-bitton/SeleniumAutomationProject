from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException


# This class defines functions that interact with the different products' pages in the AOS website.
class Products:

    def __init__(self, driver):
        self.driver = driver

    # Choose the color of the product. The function takes the chosen color as an all CAPS str in caps_color.
    # If the selected color is already selected by default, an "ElementNotInteractableException" raises.
    def choose_color(self, caps_color):
        try:
            self.driver.find_element_by_css_selector(f"#rabbit.{caps_color}").click()
        except ElementNotInteractableException:
            pass

    # Choose the quantity of a product. The function takes an int as amount.
    def choose_quantity(self, amount):
        self.driver.find_element_by_xpath("//input[@name='quantity']").send_keys(Keys.BACKSPACE + str(amount))

    # Click the "Add to Cart" button on the product page.
    def click_add_to_cart(self):
        self.driver.find_element_by_xpath("//button[@name='save_to_cart']").click()

    # Returns the name of the product as is appears in the product page.
    def product_name(self):
        return self.driver.find_element_by_css_selector("#Description>h1").text

    # Returns the price of the product as is appears in the product page.
    def product_price(self):
        return self.driver.find_element_by_css_selector("#Description>h2").text
