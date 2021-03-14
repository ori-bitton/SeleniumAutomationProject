from selenium import webdriver
from selenium.webdriver.common.by import By
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from AOS_POM.Cart import Cart
from AOS_POM.Actions import Actions
import unittest
import warnings
import openpyxl


# Testing the product data in the cart page is accurate by ordering 3 different products and quantities:
class Test5(unittest.TestCase):

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

    def test_aos5(self):
        print("AOS Test 5")
        # Defining products and quantities for the test using the excel sheet:
        chosen_cat = self.data_sheet["G2"].value
        prod1_id = self.data_sheet["G3"].value
        prod1_quan = self.data_sheet["G4"].value
        prod2_id = self.data_sheet["G6"].value
        prod2_quan = self.data_sheet["G7"].value
        prod3_id = self.data_sheet["G9"].value
        prod3_quan = self.data_sheet["G10"].value

        # Enter the category:
        self.wait.visibility((By.ID, "laptopsImg"))  # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)  # Defining a variable for the product pages.
        product.choose_quantity(prod1_quan)
        prod1_name = product.product_name()  # Defining a variable with the product's name for the assertions.
        prod1_price = product.product_price()  # Defining a variable with the product's price for the assertions.
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 2nd product:
        category.enter_product(prod2_id)
        self.wait.visibility((By.ID, "Description"))
        product.choose_quantity(prod2_quan)
        prod2_name = product.product_name()
        prod2_price = product.product_price()
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 3rd product:
        category.enter_product(prod3_id)
        self.wait.visibility((By.ID, "Description"))
        product.choose_quantity(prod3_quan)
        prod3_name = product.product_name()
        prod3_price = product.product_price()
        product.click_add_to_cart()

        # Entering the cart page:
        self.general.enter_cart_page()
        # Waiting for the cart page to load:
        self.wait.visibility((By.CLASS_NAME, "fixedTableEdgeCompatibility"))
        cart = Cart(self.driver)  # Defining a variable for the Cart class.

        # Making sure the test passed by comparing the data in the cart table to the products' info:
        # Products' quantities:
        self.assertEqual(str(prod1_quan), cart.cart_quantities(3))
        self.assertEqual(str(prod2_quan), cart.cart_quantities(2))
        self.assertEqual(str(prod3_quan), cart.cart_quantities(1))

        # Products' prices:
        # Creating a variable for every product's final price to check the site made the right calculations:
        prod1_final_price = float(prod1_price[1:]) * prod1_quan
        prod2_final_price = float(prod2_price[1:]) * prod2_quan
        prod3_final_price = float(prod3_price[1:]) * prod3_quan

        # Using a list and an IF condition for the final price test.
        # IF the price > 999, the STR needs an additional "," for the assertions to pass.
        # The list's indexes are matching the cart order.
        final_prices = [prod3_final_price, prod2_final_price, prod1_final_price]
        for i in final_prices:
            if i > 999:
                final_price_str = str(i)[0] + "," + str(i)[1:]
                self.assertEqual(f"${final_price_str}", cart.cart_prices(final_prices.index(i) + 1))
            else:
                self.assertEqual(f"${i}", cart.cart_prices(final_prices.index(i) + 1))

        # Printing the products' details for comparison:
        print(f"1st product: {prod1_name} \n   "
              f"Quantity: {prod1_quan} \n   "
              f"Price: {prod1_price} \n   "
              f"Final Price: {prod1_final_price}")
        print(f"2nd product: {prod2_name} \n   "
              f"Quantity: {prod2_quan} \n   "
              f"Price: {prod2_price} \n   "
              f"Final Price: {prod2_final_price}")
        print(f"3rd product: {prod3_name} \n   "
              f"Quantity: {prod3_quan} \n   "
              f"Price: {prod3_price} \n   "
              f"Final Price: {prod3_final_price}")

        # Writing the result in the excel sheet:
        self.data_sheet["G24"] = "V"
