import unittest
import warnings
import openpyxl
from AOS_POM.Actions import Actions
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from selenium import webdriver
from selenium.webdriver.common.by import By


# Clicking the cart icon in the upper right corner and making sure it redirects to the cart page:
class Test4(unittest.TestCase):

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

    def test_aos4(self):
        print("AOS Test 4")
        # Defining a product for the test using the excel sheet:
        chosen_cat = self.data_sheet["F2"].value
        prod1_id = self.data_sheet["F3"].value

        # Enter the category:
        self.wait.visibility((By.ID, "miceImg"))  # Wait for the homepage to load
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)  # Defining a variable for the product pages.
        product.click_add_to_cart()
        self.driver.back()

        # Entering the cart page:
        self.general.enter_cart_page()
        # Waiting for the cart page to load and the cart table to appear:
        self.wait.visibility((By.CLASS_NAME, "fixedTableEdgeCompatibility"))

        # Testing if the navigation line updated to "Shopping Cart":
        print("Desired Text: SHOPPING CART, Actual: " + self.general.nav_line(2).text)
        self.assertEqual(self.general.nav_line(2).text, "SHOPPING CART")

        # Writing the result in the excel sheet:
        self.data_sheet["F24"] = "V"
