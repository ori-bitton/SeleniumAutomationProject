from selenium import webdriver
from selenium.webdriver.common.by import By
from AOS_POM.Homepage import Homepage
from AOS_POM.General import General
from AOS_POM.Categories import Categories
from AOS_POM.Products import Products
from AOS_POM.Waiters import Waiters
from AOS_POM.Checkout import Checkout
from AOS_POM.Cart import Cart
from AOS_POM.Actions import Actions
from AOS_POM.OrderPayment import OrderPayment
import unittest
import openpyxl
import warnings


# Order a product and use an existing account in the checkout. Pay using MaterCredit
# Make sure the cart is empty and the order is under the account's "My Orders" tab.
class Test9(unittest.TestCase):

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

    def test_aos9(self):
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
        self.wait.visibility((By.ID, "tabletsImg"))  # Waiting for the homepage to load.
        Homepage(self.driver).enter_category(chosen_cat)  # Entering the chosen category.

        # Ordering product:
        category = Categories(self.driver)  # Defining a variable for the category page.
        category.enter_product(prod1_id)
        self.wait.visibility((By.ID, "Description"))  # Wait for the product description to be visible.
        product = Products(self.driver)  # Defining a variable for the product pages.
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
        checkout.click_save_changes("master_credit")  # We don't want to save the changes.
        self.wait.clickable((By.ID, "pay_now_btn_MasterCredit"))  # Waiting for the "Pay Now" button to be clickable.
        checkout.click_pay_now_mastercreadit()

        # Entering the "Thank You" page:
        payment = OrderPayment(self.driver)  # Defining a variable for the OrderPayment class.
        self.wait.visibility((By.ID, "orderPaymentSuccess"))  # Waiting for the "Thank You" page to load.
        print("Reached Thank You Page.")
        # Testing the "Thank You" massage appears properly:
        self.assertEqual("Thank you for buying with Advantage", payment.thank_you_message().text)
        order_num = payment.order_payment_num().text  # Defining a variable with the order number.

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
