import unittest
import openpyxl
import warnings
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from AOS_POM.Cart import Cart
from AOS_POM.Checkout import Checkout
from AOS_POM.CreateAccount import CreateAccount
from AOS_POM.OrderPayment import OrderPayment
from AOS_POM.Actions import Actions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class AOSTests(unittest.TestCase):

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

    # Test 1 - Order 2 different products with different quantities
    #          and check the quantity in the cart pop-up window is correct:
    def test_aos001(self):
        print("AOS Test 1")
        # Defining products and quantities for the test using the excel data sheet:
        chosen_cat = self.data_sheet["C2"].value
        prod1_id = self.data_sheet["C3"].value
        prod1_quan = self.data_sheet["C4"].value
        prod2_id = self.data_sheet["C6"].value
        prod2_quan = self.data_sheet["C7"].value

        # Enter the category:
        self.wait.visibility((By.ID, "speakersImg"))        # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)    # Enter the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)            # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product page to be load.
        product = Products(self.driver)               # Defining a variable for the product pages.
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

    # Test 2 - Order 3 different products with different quantities and colors
    #          and check the products' names, colors, quantities and prices in the pop-up window is correct:
    def test_aos002(self):
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
        self.wait.visibility((By.ID, "headphonesImg"))       # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)     # Enter the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)            # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product page to load.
        product = Products(self.driver)               # Defining a variable for the product pages.
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

    # Test 3 - Removing an item using the cart pop-up menu and testing to see it was removed properly:
    def test_aos003(self):
        print("AOS Test 3")
        # Defining products and quantities from the excel sheet for the test:
        chosen_cat = self.data_sheet["E2"].value
        prod1_id = self.data_sheet["E3"].value
        prod2_id = self.data_sheet["E6"].value

        # Enter the category:
        self.wait.visibility((By.ID, "miceImg"))                # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)        # Entering the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)                # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))      # Wait for the product description to be visible.
        product = Products(self.driver)                   # Defining a variable for the product pages.
        product.click_add_to_cart()
        self.driver.back()

        # Ordering 2nd product:
        category.enter_product(prod2_id)
        self.wait.visibility((By.ID, "Description"))
        prod2_name = product.product_name()   # Defining a variable with the product's name for the test assertions.
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

    # Test 4 - Clicking the cart icon in the upper right corner and making sure it redirects to the cart page:
    def test_aos004(self):
        print("AOS Test 4")
        # Defining a product for the test using the excel sheet:
        chosen_cat = self.data_sheet["F2"].value
        prod1_id = self.data_sheet["F3"].value

        # Enter the category:
        self.wait.visibility((By.ID, "miceImg"))             # Wait for the homepage to load
        Homepage(self.driver).enter_category(chosen_cat)     # Entering the chosen category.

        # Ordering product:
        category = Categories(self.driver)            # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)               # Defining a variable for the product pages.
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

    # Test 5 - Testing the product data in the cart page is accurate by ordering 3 different products and quantities:
    def test_aos005(self):
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
        self.wait.visibility((By.ID, "laptopsImg"))       # Wait for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering 1st product:
        category = Categories(self.driver)            # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)               # Defining a variable for the product pages.
        product.choose_quantity(prod1_quan)
        prod1_name = product.product_name()           # Defining a variable with the product's name for the assertions.
        prod1_price = product.product_price()         # Defining a variable with the product's price for the assertions.
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
        cart = Cart(self.driver)      # Defining a variable for the Cart class.

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
                self.assertEqual(f"${final_price_str}", cart.cart_prices(final_prices.index(i)+1))
            else:
                self.assertEqual(f"${i}", cart.cart_prices(final_prices.index(i)+1))

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

    # Test 6 - Testing the "Edit" function in the cart page and making sure it changes the product quantities properly:
    def test_aos006(self):
        print("AOS Test 6")
        # Defining products and quantities for the test using the excel sheet:
        chosen_cat = self.data_sheet["H2"].value
        prod1_id = self.data_sheet["H3"].value
        prod1_quan = self.data_sheet["H4"].value
        prod2_id = self.data_sheet["H6"].value
        prod2_quan = self.data_sheet["H7"].value

        # Enter the category:
        self.wait.visibility((By.ID, "laptopsImg"))        # Waiting  for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)   # Entering the laptops category.

        # Ordering 1st product:
        category = Categories(self.driver)            # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)               # Defining a variable for the product pages.
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
        self.wait.visibility((By.ID, "Description"))   # Waiting for the product page to load.
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

    # Test 7 - Adding a product from the tablets category and making sure that when you return to the previous
    #          page, it returns you to the tablets category and then to the homepage:
    def test_aos007(self):
        print("AOS Test 7")
        # Defining products and quantities for the test using the excel sheet:
        chosen_cat = self.data_sheet["I2"].value
        prod1_id = self.data_sheet["I3"].value

        # Enter the category:
        self.wait.visibility((By.ID, "tabletsImg"))          # Waiting for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)     # Entering the chosen category.

        # Ordering product:
        category = Categories(self.driver)             # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))   # Wait for the product description to be visible.
        product = Products(self.driver)                # Defining a variable for the product pages.
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

    # Test 8 - Order a product and in checkout create a new account and pay with SafPay.
    #          Make sure the payment worked, the cart is empty and the order is under the account's "My Orders" tab.
    def test_aos008(self):
        print("AOS Test 8")
        # Defining products and quantities for the test using the excel sheet:
        chosen_cat = self.data_sheet["J2"].value
        prod1_id = self.data_sheet["J3"].value

        # Defining account details and payment details using the excel sheet:
        username = self.aid_sheet["B2"].value + str(self.aid_sheet["B3"].value)   # Recreating the excel formula.
        # Updating the username index for future test executions:
        self.aid_sheet["B3"] = self.aid_sheet["B3"].value + 1
        email = self.data_sheet["J15"].value
        password = self.data_sheet["J16"].value
        safepay_user = self.data_sheet["J17"].value
        safepay_password = self.data_sheet["J18"].value

        # Enter the category:
        self.wait.visibility((By.ID, "tabletsImg"))       # Waiting for the homepage to load
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering product:
        category = Categories(self.driver)            # Defining a variable for the chosen category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)               # Defining a variable for the product pages.
        product.click_add_to_cart()

        # Waiting for the cart pop-up menu to appear and entering the checkout page:
        self.wait.visibility((By.XPATH, "//table[@ng-show='cart.productsInCart.length > 0']"))
        self.general.popup_cart_enter_checkout()
        checkout = Checkout(self.driver)  # Defining a variable for the Checkout class.

        checkout.click_register()                 # Entering the account creation page.
        new_account = CreateAccount(self.driver)  # Defining a variable for the CreateAccount class.
        # Creating a new account:
        new_account.enter_username(username)
        new_account.enter_email(email)
        new_account.enter_password_and_confirmation(password)
        new_account.agree_to_terms().click()
        # If the "agree to terms" checkbox isn't selected, it is checked again:
        if not new_account.agree_to_terms().is_selected():
            new_account.agree_to_terms().click()
        # Moving to the "Register" button, waiting for it to be clickable and clicking it:
        self.actions.move_to(new_account.register_button())
        self.wait.clickable((By.ID, "register_btnundefined"))
        new_account.register_button().click()

        # After returning to the checkout page, proceed to payment:
        self.wait.clickable((By.ID, "next_btn"))  # Waiting for the next button to be clickable.
        checkout.click_proceed_to_payment()

        # Enter SafePay details:
        checkout.choose_payment_method("safepay")
        checkout.fill_safepay_details(safepay_user, safepay_password)
        self.wait.clickable((By.ID, "pay_now_btn_SAFEPAY"))  # Wait for the "Pay Now" button to be clickable.
        checkout.click_pay_now_safepay()

        # Entering the "Thank You" page:
        payment = OrderPayment(self.driver)                   # Defining a variable for the OrderPayment class.
        self.wait.visibility((By.ID, "orderPaymentSuccess"))  # Waiting for the "Thank You" page to load.
        print("Reached Thank You Page.")
        # Testing the "Thank You" massage appears properly:
        self.assertEqual("Thank you for buying with Advantage", payment.thank_you_message().text)
        order_num = payment.order_payment_num().text          # Defining a variable with the order number.

        # Enter "my orders" and compare order number:
        self.general.open_account_menu()
        self.general.enter_my_orders()
        self.wait.visibility((By.ID, "myAccountContainer"))   # Waiting for "My Orders" page to load.
        # Searching "My Orders" page for an element with the order number.
        # If such element exists, that means the order was saved to the account.
        order_elem = self.driver.find_element_by_xpath(f"//*[text()='{order_num}']")
        self.assertEqual(order_num, order_elem.text)
        print(f"Order Number: {order_num}")

        # Entering the cart:
        self.general.enter_cart_page()
        self.wait.visibility((By.CLASS_NAME, "sticky"))  # Waiting for it to load.
        # Making sure the cart is empty:
        self.assertEqual("Your shopping cart is empty", Cart(self.driver).empty_cart().text)
        print("Shopping Cart is empty.")

        # Writing the result in the excel sheet:
        self.data_sheet["J24"] = "V"

    # Test 9 - Order a product and use an existing account in the checkout. Pay using MaterCredit
    #          Make sure the cart is empty and the order is under the account's "My Orders" tab.
    def test_aos009(self):
        print("AOS Test 9")
        # Defining products and quantities for the test using the excel sheet:
        chosen_cat = self.data_sheet["K2"].value
        prod1_id = self.data_sheet["K3"].value
        # Defining account details and payment details using the excel sheet:
        username = self.data_sheet["K12"].value
        password = self.data_sheet["K13"].value
        card = self.data_sheet["K19"].value
        cvv = self.data_sheet["K20"].value
        month = self.data_sheet["K21"].value
        year = self.data_sheet["K22"].value
        name = self.data_sheet["K23"].value

        # Enter the category:
        self.wait.visibility((By.ID, "tabletsImg"))       # Waiting for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering product:
        category = Categories(self.driver)            # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)               # Defining a variable for the product pages.
        product.click_add_to_cart()

        # Waiting for the cart pop-up menu to appear and entering the checkout page:
        self.wait.visibility((By.XPATH, "//table[@ng-show='cart.productsInCart.length > 0']"))
        self.general.popup_cart_enter_checkout()
        checkout = Checkout(self.driver)  # Defining a variable for the Checkout class.

        # Logging in to an existing account:
        checkout.fill_login_details(username, password)
        checkout.click_login()

        # Proceed to payment:
        self.wait.clickable((By.ID, "next_btn"))  # Waiting for the "Next" button to be clickable.
        checkout.click_proceed_to_payment()
        checkout.choose_payment_method("masterCredit")

        # Enter MasterCredit details:
        checkout.fill_mastercredit_details(card, cvv, month, year, name)
        checkout.click_save_changes("master_credit")              # We don't want to save the changes.
        self.wait.clickable((By.ID, "pay_now_btn_MasterCredit"))  # Waiting for the "Pay Now" button to be clickable.
        checkout.click_pay_now_mastercreadit()

        # Entering the "Thank You" page:
        payment = OrderPayment(self.driver)                   # Defining a variable for the OrderPayment class.
        self.wait.visibility((By.ID, "orderPaymentSuccess"))  # Waiting for the "Thank You" page to load.
        print("Reached Thank You Page.")
        # Testing the "Thank You" massage appears properly:
        self.assertEqual("Thank you for buying with Advantage", payment.thank_you_message().text)
        order_num = payment.order_payment_num().text          # Defining a variable with the order number.

        # Enter "my orders" and compare order number:
        self.general.open_account_menu()
        self.general.enter_my_orders()
        self.wait.visibility((By.ID, "myAccountContainer"))  # Waiting for "My Orders" page to load.
        # Searching "My Orders" page for an element with the order number.
        # If such element exists, that means the order was saved to the account.
        order_elem = self.driver.find_element_by_xpath(f"//*[text()='{order_num}']")
        self.assertEqual(order_num, order_elem.text)
        print(f"Order Number: {order_num}")

        # Entering the cart
        self.general.enter_cart_page()
        self.wait.visibility((By.CLASS_NAME, "sticky"))  # Waiting for it to load.
        # Making sure the cart is empty:
        self.assertEqual("Your shopping cart is empty", Cart(self.driver).empty_cart().text)
        print("Shopping Cart is empty.")

        # Writing the result in the excel sheet:
        self.data_sheet["K24"] = "V"

    # Test 10 - Signing in and signing out of an existing account:
    def test_aos010(self):
        print("AOS Test 10")
        # Defining username and password from an existing account using the excel sheet:
        username = self.data_sheet["L12"].value
        password = self.data_sheet["L13"].value

        # Waiting for the site to load:
        self.wait.visibility((By.ID, "tabletsImg"))

        # Opening the sign-in menu:
        self.general.open_signin_menu()
        self.wait.visibility((By.CLASS_NAME, "login"))  # Waiting for the sign-in menu to load.

        # Entering an existing account's details and signing in:
        self.general.account_signin_username(username)
        self.general.account_signin_password(password)
        self.general.click_signin_btn_account_popup()

        # Signing out of the account:
        self.wait.clickable((By.CLASS_NAME, "containMiniTitle"))    # Waiting for the user icon to be clickable.
        self.general.open_account_menu()
        self.general.click_signout_account()

        # Waiting for the username to disappear:
        self.wait.invisibility((By.CLASS_NAME, "containMiniTitle"))
        # Testing the username no longer appears and the user is signed out:
        self.assertEqual("", self.general.signed_in_username().text)
        print("User signed out")

        # Writing the result in the excel sheet:
        self.data_sheet["L24"] = "V"
