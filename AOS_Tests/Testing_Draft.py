from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from AOS_POM.Cart import Cart
from AOS_POM.Checkout import Checkout
from AOS_POM.CreateAccount import CreateAccount
from AOS_POM.OrderPayment import OrderPayment
import unittest
import openpyxl
import warnings


class AOSTestDraft(unittest.TestCase):

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
        # Defining a Waiter class and a General class for the test:
        self.wait = Waiters(self.driver)
        self.general = General(self.driver)
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

    def test_Testing(self):
        print("AOS Test")
        chosen_cat = self.data_sheet["C2"].value
        prod1_id = self.data_sheet["C3"].value
        prod1_quan = self.data_sheet["C4"].value

        self.wait.visibility((By.ID, "tabletsImg"))
        Homepage(self.driver).enter_category(chosen_cat)

        category = Categories(self.driver)
        category.enter_product(prod1_id)
        product = Products(self.driver)
        prod1_name = product.product_name()
        product.choose_quantity(prod1_quan)
        product.click_add_to_cart()

        self.wait.visibility((By.XPATH, "//table[@ng-show='cart.productsInCart.length > 0']"))

        self.assertEqual(self.general.popup_cart_name(1)[:27], prod1_name[:27])
        self.assertEqual(self.general.popup_cart_quantity(1), "QTY: " + str(prod1_quan))

        print(prod1_id)
        print(prod1_name)
        print(prod1_quan)
        self.data_sheet["M24"] = "V"
