import unittest
import warnings
import openpyxl
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from AOS_POM.Actions import Actions
from selenium import webdriver
from selenium.webdriver.common.by import By


# Order 2 different products with different quantities and check the quantity in the cart pop-up window is correct:
class Test1(unittest.TestCase):

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

    def test_aos01(self):
        print("AOS Test 1")
        # Defining products and quantities for the test using the excel data sheet:
        chosen_cat = self.data_sheet["C2"].value
        prod1_id = self.data_sheet["C3"].value
        prod1_quan = self.data_sheet["C4"].value
        prod2_id = self.data_sheet["C6"].value
        prod2_quan = self.data_sheet["C7"].value

        # Enter the category:
        self.wait.visibility((By.ID, "speakersImg"))  # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Enter the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product page to be load.
        product = Products(self.driver)  # Defining a variable for the product pages.
        product.choose_quantity(prod1_quan)
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 2nd product:
        category.enter_product(prod2_id)
        self.wait.visibility((By.ID, "Description"))
        product.choose_quantity(prod2_quan)
        product.click_add_to_cart()

        # Waiting for the cart pop-up menu to appear before the assertions stage:
        self.wait.clickable((By.ID, "checkOutPopUp"))

        # Printing the result for comparison.
        print(f"Product 1 Desired QTY: {prod1_quan}, Actual {self.general.popup_cart_quantity(2)}")
        print(f"Product 2 Desired QTY: {prod2_quan}, Actual {self.general.popup_cart_quantity(1)}")
        # Making sure the test passed using the products' quantity variable and a General class function.
        self.assertEqual(str(f"QTY: {prod1_quan}"), self.general.popup_cart_quantity(2))
        self.assertEqual(str(f"QTY: {prod2_quan}"), self.general.popup_cart_quantity(1))

        # Writing the result in the excel sheet:
        self.data_sheet["C24"] = "V"
