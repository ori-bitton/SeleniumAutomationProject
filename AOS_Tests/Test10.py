from selenium import webdriver
from selenium.webdriver.common.by import By
from AOS_POM.General import General
from AOS_POM.Waiters import Waiters
from AOS_POM.Actions import Actions
import openpyxl
import warnings
import unittest


# Signing in and signing out of an existing account:
class Test10(unittest.TestCase):

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

    def test_aso10(self):
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
        self.wait.clickable((By.CLASS_NAME, "containMiniTitle"))  # Waiting for the user icon to be clickable.
        self.general.open_account_menu()
        self.general.click_signout_account()

        # Waiting for the username to disappear:
        self.wait.invisibility((By.CLASS_NAME, "containMiniTitle"))
        # Testing the username no longer appears and the user is signed out:
        self.assertEqual("", self.general.signed_in_username().text)
        print("User signed out")

        # Writing the result in the excel sheet:
        self.data_sheet["L24"] = "V"
