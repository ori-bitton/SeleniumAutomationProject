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
from selenium.common.exceptions import NoSuchElementException


# Removing an item using the cart pop-up menu and testing to see it was removed properly:
class Test3(unittest.TestCase):

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

    def test_aos3(self):
        print("AOS Test 3")
        # Defining products and quantities from the excel sheet for the test:
        chosen_cat = self.data_sheet["E2"].value
        prod1_id = self.data_sheet["E3"].value
        prod2_id = self.data_sheet["E6"].value

        # Enter the category:
        self.wait.visibility((By.ID, "miceImg"))  # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)  # Defining a variable for the product pages.
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 2nd product:
        category.enter_product(prod2_id)
        self.wait.visibility((By.ID, "Description"))
        prod2_name = product.product_name()  # Defining a variable with the product's name for the test assertions.
        product.click_add_to_cart()

        # Waiting for the cart pop-up menu to appear and removing a product:
        self.wait.visibility((By.XPATH, "//table[@ng-show='cart.productsInCart.length > 0']"))
        self.general.popup_cart_remove_product(2)

        # Making sure you can't delete the 2nd item in the cart after it's been deleted:
        with self.assertRaises(NoSuchElementException):
            self.general.popup_cart_remove_product(2)

        # Hovering over the cart icon and waiting for the pop-up menu to appear:
        self.general.hover_cart_icon()
        self.wait.visibility((By.XPATH, "//table[@ng-show='cart.productsInCart.length > 0']"))

        # Making sure the item left in the cart is the correct one:
        print(f"Desired product left: {prod2_name}")
        print(f"Actual product left: {self.general.popup_cart_name(1)}")
        self.assertEqual(prod2_name, self.general.popup_cart_name(1))

        # Writing the result in the excel sheet:
        self.data_sheet["E24"] = "V"
