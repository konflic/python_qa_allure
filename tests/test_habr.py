import allure
import pytest

from page_objects.HabrObject import HabrObject


@allure.title("Проврека перехода в статью из поиска")
def test_post_open(driver):
    page = HabrObject(driver)
    page.open()
    page.click_search()
    page.search('Python')
    page.read_more()
    page.is_present(page.POST_BODY)


@pytest.mark.parametrize("req", ["Python", "Java"])
@allure.title("Проверка перехода в раздел хабов")
def test_hubs_open(driver, req):
    page = HabrObject(driver)
    page.open()
    page.click_search()
    page.search(req)
    page.select_hubs()
    page.is_present(page.HUBS)
