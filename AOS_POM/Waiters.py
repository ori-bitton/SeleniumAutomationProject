from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# This class makes the WebDriverWait class in Selenium more accessible.
class Waiters:

    # The class needs a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # Wait until an element is visible. by_element_tup is a tuple: (By.LOCATOR, "html path")
    def visibility(self, by_element_tup):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_element_tup))

    # Wait until an element is clickable. by_element_tup is a tuple: (By.LOCATOR, "html path")
    def clickable(self, by_element_tup):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_element_tup))

    # Wait until an element is invisible. by_element_tup is a tuple: (By.LOCATOR, "html path")
    def invisibility(self, by_element_tup):
        return WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(by_element_tup))
