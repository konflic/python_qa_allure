import time
import allure
import pytest


@allure.step("Выполняю клик по элементу")
def click_element(driver, selector):
    driver.find_element_by_css_selector(selector).click()


@allure.step("Ввожу '{text}' в элемент {selector}")
def input_text(driver, selector, text):
    driver.find_element_by_css_selector(selector).send_keys(text)


@allure.step("Открываю url {url}")
def open_page(driver, url):
    driver.get(url)


def test_one(local_browser):
    open_page(local_browser, "https://ya.ru")
    input_text(local_browser, "#text", "Привет")
    click_element(local_browser, "[role='button']")
    time.sleep(2)


@pytest.mark.parametrize("text", ["Привет", "", 1234])
def test_two(local_browser, text):
    url = "https://ya.ru"
    input_field = "#text"
    with allure.step(f"Открываю страницу {url}"):
        local_browser.get(url)
    with allure.step(f"Ввожу значение {text} в {input_field}"):
        local_browser.find_element_by_css_selector(input_field).send_keys(text)
    time.sleep(2)
