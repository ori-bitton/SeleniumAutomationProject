# This class defines functions that interact with elements in the "Order Payment" page in the AOS website.
class OrderPayment:

    # The class needs a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # Returns the "Thank you for buying with Advantage" massage element:
    def thank_you_message(self):
        return self.driver.find_element_by_css_selector("#orderPaymentSuccess>h2>span")

    # Returns the order number from the order payment page:
    def order_payment_num(self):
        return self.driver.find_element_by_id("orderNumberLabel")
