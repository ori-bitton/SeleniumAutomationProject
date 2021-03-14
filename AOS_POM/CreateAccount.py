# This class defines functions that interact with elements in the account creation page:
class CreateAccount:

    # The class needs a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # A function that fills the username in the new account creation page:
    def enter_username(self, username):
        self.driver.find_element_by_css_selector("input[name='usernameRegisterPage']").send_keys(f"{username}")

    # A function that fills the password and password confirmation in the new account creation page:
    def enter_password_and_confirmation(self, password):
        self.driver.find_element_by_css_selector("input[name='passwordRegisterPage']").send_keys(f"{password}")
        self.driver.find_element_by_css_selector("input[name='confirm_passwordRegisterPage']").send_keys(f"{password}")

    # A function that fills the email in the new account creation page:
    def enter_email(self, email):
        self.driver.find_element_by_css_selector("input[name='emailRegisterPage']").send_keys(f"{email}")

    # A function that clicks the site terms agreement checkbox:
    def agree_to_terms(self):
        return self.driver.find_element_by_css_selector("input[name='i_agree']")

    # A function that clicks the "Register" button:
    def register_button(self):
        return self.driver.find_element_by_id("register_btnundefined")
