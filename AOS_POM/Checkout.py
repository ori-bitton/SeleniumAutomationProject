from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# This class defines functions that interact with elements in the checkout page in the AOS website:
class Checkout:

    # The class needs a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # A function that fills in the details of an existing account (username and password):
    def fill_login_details(self, username, password):
        self.driver.find_element_by_css_selector("input[name='usernameInOrderPayment']").send_keys(f"{username}")
        self.driver.find_element_by_css_selector("input[name='passwordInOrderPayment']").send_keys(f"{password}")

    # A function that clicks the login button and enters a registered account:
    # Must fill in the login details in the website before.
    def click_login(self):
        self.driver.find_element_by_id("login_btnundefined").click()

    # A function that clicks the "Register" button and redirects you to the account creation page:
    def click_register(self):
        self.driver.find_element_by_id("registration_btnundefined").click()

    # A function that proceeds to payment after signing in by clicking the "Next" button:
    def click_proceed_to_payment(self):
        self.driver.find_element_by_id("next_btn").click()

    # Choose the payment method. method = "safepay" / "masterCredit".
    # Only after the user logged in an account and clicked proceed to payment.
    def choose_payment_method(self, method):
        self.driver.find_element_by_css_selector(f"input[name='{method}']").click()

    # A function that fills your safepay details: username and password.
    def fill_safepay_details(self, username, password):
        self.driver.find_element_by_css_selector("input[name='safepay_username']").send_keys(f"{username}")
        self.driver.find_element_by_css_selector("input[name='safepay_password']").send_keys(f"{password}")

    # A function that fills your masterCredit details: card_num (card number), cvv, month, year, name (of cardholder).
    def fill_mastercredit_details(self, card_num, cvv, month, year, name):
        self.driver.find_element_by_id("creditCard").send_keys(f"{card_num}")
        self.driver.find_element_by_css_selector("input[name='cvv_number']").send_keys(f"{cvv}")
        self.driver.find_element_by_css_selector("input[name='cardholder_name']").send_keys(f"{name}")
        # The date in the website is a drop down menu:
        mm = Select(self.driver.find_element_by_css_selector("select[name='mmListbox']"))
        mm.select_by_visible_text(str(month))
        yyyy = Select(self.driver.find_element_by_css_selector("select[name='yyyyListbox']"))
        yyyy.select_by_visible_text(str(year))

        # Because of the speed of the automation, the CVV isn't entered correctly sometimes.
        # To override this problem, the function will try to find the "Invalid CVV" element.
        # If the element is found, it will fill in the CVV again
        # If not - it will continue with the program.
        try:
            self.driver.find_element_by_css_selector("sec-view>div>label.invalid")
            self.driver.find_element_by_css_selector("input[name='cvv_number']").clear()
            self.driver.find_element_by_css_selector("input[name='cvv_number']").send_keys(f"{cvv}")
        except NoSuchElementException:
            pass

    # A function that clicks the "Save Changes" checkbox in the checkout.
    # The function receives the payment method in the payment variable: "safepay" or "master_credit".
    def click_save_changes(self, payment):
        self.driver.find_element_by_css_selector(f"input[name='save_{payment}']").click()

    # A function that clicks the "Pay Now" button with SafePay:
    def click_pay_now_safepay(self):
        self.driver.find_element_by_id("pay_now_btn_SAFEPAY").click()

    # A function that clicks the "Pay Now" button with MaterCredit:
    def click_pay_now_mastercreadit(self):
        self.driver.find_element_by_id("pay_now_btn_MasterCredit").click()
