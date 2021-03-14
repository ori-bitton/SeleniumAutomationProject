# This class defines functions that interact with the homepage in the AOS website.
class Homepage:

    # The class need a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # Enter the speakers category from the homepage.
    def enter_speakers_cat(self):
        self.driver.find_element_by_id("speakersImg").click()

    # Enter the laptops category from the homepage.
    def enter_laptops_cat(self):
        self.driver.find_element_by_id("laptopsImg").click()

    # Enter the headphones category from the homepage.
    def enter_headphones_cat(self):
        self.driver.find_element_by_id("headphonesImg").click()

    # Enter the tablets category from the homepage.
    def enter_tablets_cat(self):
        self.driver.find_element_by_id("tabletsImg").click()

    # Enter the mice category from the homepage.
    def enter_mice_cat(self):
        self.driver.find_element_by_id("miceImg").click()

    # Dynamic function for entering every category.
    # Takes the category name as "category" variable. Must be all low letters.
    def enter_category(self, category):
        self.driver.find_element_by_id(f"{category}Img").click()
