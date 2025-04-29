from random import random
import selectors
import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


class Page:

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Выполняю клик по элементу {selector}")
    def click_element(self, selector):
        self.driver.find_element(By.CSS_SELECTOR, selector).click()

    @allure.step("Ввожу '{text}' в элемент {selector}")
    def input_text(self, selector, text):
        self.driver.find_element(By.CSS_SELECTOR, selector).send_keys(text)

    @allure.step("Проверяю что элемент {selector} видим пользователю")
    def check_visibility(self, selector):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    @allure.step("Открываю url {url}")
    def open_page(self, url):
        self.driver.get(url)


def test_step_example(driver):
    page = Page(driver)
    page.open_page("http://192.168.0.119:8081/")
    page.input_text("#search input", "MacBook")
    page.click_element("#search button")
    page.check_visibility("#product-list")


@pytest.mark.parametrize("text", ["MacBook", "iPhone", "Canon"])
def test_with_step_example(driver, text):
    page = Page(driver)
    input_field = "#search input"

    with allure.step(f"Открыаю url и выполняю поиск {input_field}"):
        page.open_page("http://192.168.0.119:8081/")

        with allure.step(f"Ввожу значение {text} в {input_field}"):
            page.input_text(input_field, text)

        with allure.step("Нажимаю Поиск"):
            page.click_element("#search button")

    with allure.step("Проверяю что отображаются результаты поиска"):
        page.check_visibility("#product-list")
