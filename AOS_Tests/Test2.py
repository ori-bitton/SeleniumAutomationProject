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


# Order 3 different products with different quantities and colors
# and check the products' names, colors, quantities and prices in the pop-up window is correct:
class Test2(unittest.TestCase):

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

    def test_aos2(self):
        print("AOS Test 2")
        # Defining products, colors and quantities for the test using the excel data sheet:
        chosen_cat = self.data_sheet["D2"].value
        prod1_id = self.data_sheet["D3"].value
        prod1_quan = self.data_sheet["D4"].value
        prod1_color = self.data_sheet["D5"].value
        prod2_id = self.data_sheet["D6"].value
        prod2_quan = self.data_sheet["D7"].value
        prod2_color = self.data_sheet["D8"].value
        prod3_id = self.data_sheet["D9"].value
        prod3_quan = self.data_sheet["D10"].value
        prod3_color = self.data_sheet["D11"].value

        # Enter the category:
        self.wait.visibility((By.ID, "headphonesImg"))  # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Enter the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product page to load.
        product = Products(self.driver)  # Defining a variable for the product pages.
        # Creating a variable with the product's name for the testing assertions:
        prod1_name = product.product_name()
        # Creating a variable with the product's unit price for the testing assertions:
        prod1_price = product.product_price()
        product.choose_color(prod1_color)
        product.choose_quantity(prod1_quan)
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 2nd product:
        category.enter_product(prod2_id)
        self.wait.visibility((By.ID, "Description"))
        prod2_name = product.product_name()
        prod2_price = product.product_price()
        product.choose_color(prod2_color)
        product.choose_quantity(prod2_quan)
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 3rd product:
        category.enter_product(prod3_id)
        self.wait.visibility((By.ID, "Description"))
        prod3_name = product.product_name()
        prod3_price = product.product_price()
        product.choose_color(prod3_color)
        product.choose_quantity(prod3_quan)
        product.click_add_to_cart()

        # Waiting for the cart pop-up menu to appear before the assertions stage:
        self.wait.visibility((By.XPATH, "//table[@ng-show='cart.productsInCart.length > 0']"))

        # Printing the test data for compairson:
        print(f"Product 1:\n"
              f"Name: Desired - {prod1_name}, Actual - {self.general.popup_cart_name(3)} \n"
              f"Color: Desired - {prod1_color}, Actual - {self.general.popup_cart_color(3)[7:]} \n"
              f"Quantity: Desired - {prod1_quan}, Actual - {self.general.popup_cart_quantity(3)[5:]} \n"
              f"Price: Desired - {prod1_price} * {str(prod1_quan)}, Actual - {self.general.popup_cart_price(3)}")
        print(f"Product 2:\n"
              f"Name: Desired - {prod2_name}, Actual - {self.general.popup_cart_name(2)} \n"
              f"Color: Desired - {prod2_color}, Actual - {self.general.popup_cart_color(2)[7:]} \n"
              f"Quantity: Desired - {prod2_quan}, Actual - {self.general.popup_cart_quantity(2)[5:]} \n"
              f"Price: Desired - {prod2_price} * {str(prod2_quan)}, Actual - {self.general.popup_cart_price(2)}")
        print(f"Product 3:\n"
              f"Name: Desired - {prod3_name}, Actual - {self.general.popup_cart_name(1)} \n"
              f"Color: Desired - {prod3_color}, Actual - {self.general.popup_cart_color(1)[7:]} \n"
              f"Quantity: Desired - {prod3_quan}, Actual - {self.general.popup_cart_quantity(1)[5:]} \n"
              f"Price: Desired - {prod3_price} * {str(prod3_quan)}, Actual - {self.general.popup_cart_price(1)}")
        # Making sure the test passed using the prod variables and General class functions:

        # Pop-up cart names = Products' names:
        # List with all the prod_name variables sorted according to their order in the cart.
        names_list = [prod3_name, prod2_name, prod1_name]
        for i in names_list:
            # Because the cart pop-up menu shortens product names > 27 letters, the assertion has an IF condition:
            # IF the product name is > 27, only the first 27 letters are used for the assertion.
            if len(i) > 27:
                self.assertEqual(i[0:27], self.general.popup_cart_name(names_list.index(i) + 1)[0:27])
            else:
                self.assertEqual(i, self.general.popup_cart_name(names_list.index(i) + 1))

        # Pop-up cart colors = Products' colors:
        self.assertEqual(f"Color: {prod1_color}", self.general.popup_cart_color(3))
        self.assertEqual(f"Color: {prod2_color}", self.general.popup_cart_color(2))
        self.assertEqual(f"Color: {prod3_color}", self.general.popup_cart_color(1))

        # Pop-up cart quantity = Products' quantity:
        self.assertEqual(f"QTY: {prod1_quan}", self.general.popup_cart_quantity(3))
        self.assertEqual(f"QTY: {prod2_quan}", self.general.popup_cart_quantity(2))
        self.assertEqual(f"QTY: {prod3_quan}", self.general.popup_cart_quantity(1))

        # Pop-up cart price = Products' price:
        # Every product's unit price is converted to a float and multiplied by the ordered quantity,
        # then it's compared to the pop-up menu's final price (also converted to float and removed the "$").
        self.assertEqual(float(prod1_price[1:]) * prod1_quan, float(self.general.popup_cart_price(3)[1:]))
        self.assertEqual(float(prod2_price[1:]) * prod2_quan, float(self.general.popup_cart_price(2)[1:]))
        self.assertEqual(float(prod3_price[1:]) * prod3_quan, float(self.general.popup_cart_price(1)[1:]))

        # Writing the result in the excel sheet:
        self.data_sheet["D24"] = "V"
