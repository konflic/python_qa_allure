from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


class BasePage:

    def __init__(self, driver, wait=2):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait)

    def _open(self, url):
        self.driver.get(url)
        return self

    def click(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator)).click()
            return self
        except TimeoutException:
            raise TimeoutException

    def input_and_submit(self, locator, value):
        find_field = self.driver.find_element(*locator)
        find_field.send_keys(value)
        find_field.send_keys(Keys.ENTER)
        return self

    def is_present(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException
