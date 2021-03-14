import unittest
import openpyxl
import warnings
from AOS_POM.Actions import Actions
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# Adding a product from the tablets category and making sure that when you return to the previous page,
# it returns you to the tablets category and then to the homepage:
class Test7(unittest.TestCase):

    def setUp(self):
        print("--- Set Up ---")
        # Defining the variables that will access the data in the excel sheet:
        self.data_book = openpyxl.load_workbook("C:/Users/ori/Selenium/AOSTestData.xlsx")
        self.data_sheet = self.data_book["Data"]
        self.aid_sheet = self.data_book["Aids"]
        # Defining a Chrome browser and 10 seconds implicit wait:
        self.driver = webdriver.Chrome(executable_path=str(self.aid_sheet["C4"].value))
        self.driver.implicitly_wait(10)
        # Entering the AOS website:
        self.driver.get("http://advantageonlineshopping.com/#/")
        self.driver.maximize_window()
        # Defining a Waiter class, Actions class and a General class for the test:
        self.wait = Waiters(self.driver)
        self.general = General(self.driver)
        self.actions = Actions(self.driver)
        # Ignore the "tracemalloc" ResourceWarning:
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        print("--- Tear Down ---")
        # Return to homepage:
        self.general.click_logo_button()
        self.wait.visibility((By.ID, "speakersImg"))  # Wait for the homepage to load.
        # Closing the browser:
        self.driver.close()
        # Saving the excel book:
        self.data_book.save("C:/Users/ori/Selenium/AOSTestData.xlsx")

    def test_aos7(self):
        print("AOS Test 7")
        # Defining products and quantities for the test using the excel sheet:
        chosen_cat = self.data_sheet["I2"].value
        prod1_id = self.data_sheet["I3"].value

        # Enter the category:
        self.wait.visibility((By.ID, "tabletsImg"))  # Waiting for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)  # Defining a variable for the product pages.
        product.click_add_to_cart()

        # Return to the tablets category page:
        self.driver.back()

        # Making sure we returned to the tablets category page and the navigation line updated:
        print(f"Desired navigation line indication: TABLETS, Actual: {self.general.nav_line(2).text}")
        self.assertEqual("TABLETS", self.general.nav_line(2).text)
        # Making sure we can't go to a product's page using the navigation line:
        with self.assertRaises(NoSuchElementException):
            self.general.nav_line(3).click()

        # Return to the homepage:
        self.driver.back()

        # Making sure we returned to the homepage and the navigation line disappeared:
        with self.assertRaises(NoSuchElementException):
            self.general.nav_line(2).click()
        print("Returned to Homepage")

        # Writing the result in the excel sheet:
        self.data_sheet["I24"] = "V"
