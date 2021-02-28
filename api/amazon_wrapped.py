from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

_COUNTRIES = ['USD', 'COP']


class AmazonWrapped:
    def __init__(self):
        self.web_driver = webdriver.Chrome(ChromeDriverManager().install())
        self.action = ActionChains(self.web_driver)

    def login(self, email: str, password: str):

        self.web_driver.get("http://www.amazon.com")

        try:
            first_level_menu = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#nav-link-accountList")))
            action = ActionChains(self.web_driver)
            action.move_to_element(first_level_menu).perform()
        except Exception as e:
            print(e)

        self.web_driver.find_element_by_xpath('//*[@id="nav-flyout-ya-signin"]/a/span').click()
        self.web_driver.find_element_by_xpath('//*[@id="ap_email"]').send_keys(email)
        self.web_driver.find_element_by_xpath('//*[@id="continue"]').click()
        self.web_driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys(password)
        self.web_driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()

    def check_cards_balance(self):
        self.web_driver.find_element_by_xpath('//*[@id="asv-gclp-balance-widget-desktop"]/ul/li[1]/span/a').click()

    def move_to_cards(self):
        self.web_driver.find_element_by_xpath('//*[@id="nav-xshop"]/a[6]').click()

    def redeem_card(self, gift_card: str):
        self.web_driver.find_element_by_xpath('//*[@id="a-autoid-1-announce"]').click()
        self.web_driver.find_element_by_xpath('//*[@id="gc-redemption-input"]').send_keys(gift_card)
        self.web_driver.find_element_by_xpath('//*[@id="gc-redemption-apply-button"]').click()

    def get_card_balance(self):
        data = self.web_driver.find_element_by_xpath('//*[@id="gc-current-balance"]').get_attribute(
            'innerHTML').replace('\n', '').strip()
        return data

    def get_actual_balance(self) -> float:
        try:
            data = self.web_driver.find_element_by_xpath('//*[@id="gc-current-balance"]').get_attribute(
                'innerHTML').replace('\n', '').strip()
        except:
            data = self.web_driver.find_element_by_xpath('//*[@id="gc-ui-balance-gc-balance-value"]' ).get_attribute(
                'innerHTML').replace('\n', '').strip()
        for country in _COUNTRIES:
            data = data.strip(country)
        return float(data)

    def check_if_redeem(self):
        try:
            self.web_driver.find_element_by_xpath('//*[@id="gc-redemption-error"]')
            error = self.web_driver.find_element_by_xpath('//*[@id="gc-redemption-error"]/div/div').get_attribute(
                'innerHTML').replace('\n', '').strip()
            error = error.split('<a')[0]
            return False, error
        except NoSuchElementException:
            self.web_driver.find_element_by_xpath('//*[@id="alertRedemptionSuccess"]')
            val = self.get_card_balance()
            return True, val
