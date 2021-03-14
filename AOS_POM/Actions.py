from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# The class defines functions that perform different actions in the browser or AOS website:
class Actions:

    # The class needs a Selenium driver to work:
    def __init__(self, driver):
        self.driver = driver

    # Scroll down anywhere in the browser:
    def scroll_down(self):
        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()

    # A function that moves to an element in the website:
    def move_to(self, element):
        ActionChains(self.driver).move_to_element(element).perform()
