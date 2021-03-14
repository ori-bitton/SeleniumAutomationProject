from selenium import webdriver
from selenium.webdriver.common.by import By
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from AOS_POM.Cart import Cart
from AOS_POM.Actions import Actions
import openpyxl
import warnings
import unittest


# Testing the "Edit" function in the cart page and making sure it changes the product quantities properly:
class Test6(unittest.TestCase):

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

    def test_aos6(self):
        print("AOS Test 6")
        # Defining products and quantities for the test using the excel sheet:
        chosen_cat = self.data_sheet["H2"].value
        prod1_id = self.data_sheet["H3"].value
        prod1_quan = self.data_sheet["H4"].value
        prod2_id = self.data_sheet["H6"].value
        prod2_quan = self.data_sheet["H7"].value

        # Enter the category:
        self.wait.visibility((By.ID, "laptopsImg"))  # Waiting  for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the laptops category.

        # Ordering 1st product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)  # Defining a variable for the product pages.
        product.choose_quantity(prod1_quan)
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 2nd product:
        category.enter_product(prod2_id)
        self.wait.visibility((By.ID, "Description"))
        product.choose_quantity(prod2_quan)
        product.click_add_to_cart()

        # Entering the cart page:
        self.general.enter_cart_page()
        # Waiting for the cart page to load:
        self.wait.visibility((By.CLASS_NAME, "fixedTableEdgeCompatibility"))
        cart = Cart(self.driver)  # Defining a variable for the Cart class.

        # Editing the 1st product's quantity:
        cart.cart_click_edit(2)
        self.wait.visibility((By.ID, "Description"))  # Waiting for the product page to load.
        product.choose_quantity(prod1_quan + 1)
        product.click_add_to_cart()

        # Waiting for the cart page to load:
        self.wait.visibility((By.CLASS_NAME, "fixedTableEdgeCompatibility"))

        # Editing the 2nd product's quantity:
        # Waiting for the cart popup menu to disappear:
        self.wait.invisibility((By.CSS_SELECTOR, "table[ng-show='cart.productsInCart.length > 0']"))
        cart.cart_click_edit(1)
        self.wait.visibility((By.ID, "Description"))
        product.choose_quantity(prod2_quan + 1)
        product.click_add_to_cart()

        # Waiting for the cart page to load:
        self.wait.visibility((By.CLASS_NAME, "fixedTableEdgeCompatibility"))

        # Printing for comparison:
        print(f"Product 1 desired quantity: {prod1_quan + 1}")
        print(f"Product 1 actual quantity: {cart.cart_quantities(2)}")
        print(f"Product 2 desired quantity: {prod2_quan + 1}")
        print(f"Product 2 actual quantity: {cart.cart_quantities(1)}")
        # Making sure the test passed by comparing the quantity in the cart page to the new wanted quantity:
        self.assertEqual(cart.cart_quantities(2), str(prod1_quan + 1))
        self.assertEqual(cart.cart_quantities(1), str(prod2_quan + 1))

        # Writing the result in the excel sheet:
        self.data_sheet["G24"] = "V"
