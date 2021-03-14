from selenium.webdriver.common.action_chains import ActionChains


# This class defines functions that interact with global elements in the AOS website.
class General:

    # The class needs a Selenium driver to work.
    def __init__(self, driver):
        self.driver = driver

    # Click and open the sign in menu in the upper right corner:
    def open_signin_menu(self):
        self.driver.find_element_by_id("menuUser").click()

    # Enter the shopping cart page:
    def enter_cart_page(self):
        self.driver.find_element_by_id("shoppingCartLink").click()

    # Hover over the cart icon in the upper right corner to open the cart pop up menu:
    def hover_cart_icon(self):
        ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("shoppingCartLink")).perform()

    # A function that returns the quantity of a product in the cart pop up menu as : "QTY: X".
    # The function receives the number of the product in the cart (by order of purchase) as prod_cart_num.
    def popup_cart_quantity(self, prod_cart_num):
        return self.driver.find_element_by_xpath(f"//table[@ng-show='cart.productsInCart.length > 0'] \
                                                        /tbody/tr[{prod_cart_num}]/td[2]/a/label[1]").text

    # A function that returns the color of a product in the cart pop up menu as : "Color: X".
    # The function receives the number of the product in the cart (by order of purchase) as prod_cart_num.
    def popup_cart_color(self, prod_cart_num):
        return self.driver.find_element_by_xpath(f"//table[@ng-show='cart.productsInCart.length > 0'] \
                                                        /tbody/tr[{prod_cart_num}]/td[2]/a/label[2]").text

    # A function that returns the name of a product in the cart pop up menu as it appears there.
    # ATTENTION - The site shortens product names > 27 to 27 letters and adds "..." at the end (total 30 chars).
    # The function receives the number of the product in the cart (by order of purchase) as prod_cart_num.
    def popup_cart_name(self, prod_cart_num):
        return self.driver.find_element_by_xpath(f"//table[@ng-show='cart.productsInCart.length > 0'] \
                                                     /tbody/tr[{prod_cart_num}]/td[2]/a/h3[@class='ng-binding']").text

    # A function that returns the price of a product in the cart pop up menu (unit price * quantity).
    # The returned str appears as: "$XXX.XX" / "$X,XXX.XX"
    # The function receives the number of the product in the cart (by order of purchase) as prod_cart_num.
    def popup_cart_price(self, prod_cart_num):
        return self.driver.find_element_by_xpath(f"//table[@ng-show='cart.productsInCart.length > 0'] \
                                                        /tbody/tr[{prod_cart_num}]/td[3]/p").text

    # Remove a product from the cart using the cart pop-up menu in the upper right corner.
    # The function receives the number of the product in the cart (by order of purchase) as prod_cart_num.
    def popup_cart_remove_product(self, prod_cart_num):
        self.driver.find_element_by_xpath(f"//table[@ng-show='cart.productsInCart.length > 0'] \
                                                        /tbody/tr[{prod_cart_num}]/td[3]/div/div").click()

    # Enter a product's page using the cart pop-up menu:
    def popup_cart_click_product(self, prod_cart_num):
        self.driver.find_element_by_xpath(f"//table[@ng-show='cart.productsInCart.length > 0']\
                                                        /tbody/tr[{prod_cart_num}]").click()

    # Enter the checkout page using the cart pop-up menu:
    def popup_cart_enter_checkout(self):
        self.driver.find_element_by_id("checkOutPopUp").click()

    # Click the AOS logo in the upper left corner of the screen to return to the homepage:
    def click_logo_button(self):
        self.driver.find_element_by_css_selector(".logo>a[role='link']").click()

    # Returns a chosen element in the navigation line.
    # The location variable specifies the wanted element by order of appearance in the navigation line (1, 2, 3...).
    def nav_line(self, location):
        return self.driver.find_element_by_xpath(f"//nav/a[{location}]")

    # Open the account pop-up menu when you are signed in:
    def open_account_menu(self):
        self.driver.find_element_by_class_name("containMiniTitle").click()

    # Enter "My Orders" in the account pop-up menu un the upper right corner:
    # Works only when the account pop-up menu is open.
    def enter_my_orders(self):
        self.driver.find_element_by_xpath("//a[@id='menuUserLink']/div/label[2]").click()

    # Fill in the username in the account pop-up menu:
    def account_signin_username(self, username):
        self.driver.find_element_by_css_selector(".ng-pristine[name='username']").send_keys(f"{username}")

    # Fill in the password in the account pop-up menu:
    def account_signin_password(self, password):
        self.driver.find_element_by_css_selector(".ng-pristine[name='password']").send_keys(f"{password}")

    # Click the "Sign-In" button in the account pop-up menu:
    def click_signin_btn_account_popup(self):
        self.driver.find_element_by_id("sign_in_btnundefined").click()

    # Click the "Sign Out" button in the account menu:
    def click_signout_account(self):
        self.driver.find_element_by_css_selector("#loginMiniTitle>label[translate='Sign_out']").click()

    # Returns the element with the username that is signed in:
    def signed_in_username(self):
        return self.driver.find_element_by_class_name("containMiniTitle")
