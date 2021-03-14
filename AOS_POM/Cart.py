# This class defines functions that interact with the cart page in the AOS website.
class Cart:

    # The class needs a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # Returning the cart table element.
    def cart_table(self):
        return self.driver.find_element_by_class_name("fixedTableEdgeCompatibility")

    # Returns the name of a product in the cart table.
    # The function takes the prod_cart_num variable that specifies the order of the product in the cart.
    def cart_names(self, prod_cart_num):
        return self.cart_table().find_element_by_xpath(f"//tbody/tr[{prod_cart_num}]/td[2]/label").text

    # Returns the price of a product in the cart table (unit price * quantity) as : "$XXX.XX" / "$X,XXX.XX"
    # The function takes the prod_cart_num variable that specifies the order of the product in the cart.
    def cart_prices(self, prod_cart_num):
        return self.cart_table().find_element_by_xpath(f"//tbody/tr[{prod_cart_num}]/td[6]/p").text

    # Returns the quantity of a product in the cart table as a string.
    # The function takes the prod_cart_num variable that specifies the order of the product in the cart.
    def cart_quantities(self, prod_cart_num):
        return self.cart_table().find_element_by_xpath(f"//tbody/tr[{prod_cart_num}] \
                                                            /td[5]/label[@class='ng-binding']").text

    # The function returns the total cart's price as : "@XXX.XX" / "$X,XXX.XX"
    def cart_total_price(self):
        return self.driver.find_element_by_css_selector(".fixedTableEdgeCompatibility>tfoot>\
                                                            tr>td[colspan='2']>span.roboto-medium").text

    # A function that clicks the checkout button element in the cart page:
    def cart_checkout(self):
        self.driver.find_element_by_id("checkOutButton").click()

    # A function that clicks the edit button for a specific product in the cart page.
    # prod_cart_num variable takes the number of the wanted product in the cart.
    def cart_click_edit(self, prod_cart_num):
        self.cart_table().find_element_by_xpath(f"//tbody/tr[{prod_cart_num}]/td[6]/span/a[1]").click()

    # A function that clicks the remove button for a specific product in the cart page.
    # prod_cart_num variable takes the number of the wanted product in the cart.
    def cart_remove_click(self, prod_cart_num):
        self.cart_table().find_element_by_xpath(f"//tbody/tr[{prod_cart_num}]/td[6]/span/a[3]").click()

    # A function that returns the element that appears when the cart is empty:
    def empty_cart(self):
        return self.driver.find_element_by_css_selector(".bigEmptyCart>label")
