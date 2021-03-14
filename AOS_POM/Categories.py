# This class defines functions that interact with the different categories' pages in the AOS website.
class Categories:

    # The class needs a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # Click the "Buy Now" button in the category that redirects you to the best selling product of that category.
    def buy_now(self):
        self.driver.find_element_by_css_selector("button[name='buy_now']").click()

    # Enter a product in the category. The function takes the product ID as product_id.
    def enter_product(self, product_id):
        self.driver.find_element_by_css_selector(f"img[id='{product_id}']").click()
