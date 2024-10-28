import allure

from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By


class HabrObject(BasePage):
    URL = "https://habr.com/en"
    SEARCH_ICON = (By.CSS_SELECTOR, ".tm-header-user-menu__search .tm-header-user-menu__icon_search")
    SEARCH_FILED = (By.CSS_SELECTOR, "input[name='q']")
    READ_MORE = (By.CSS_SELECTOR, ".tm-article-snippet__readmore")
    # READ_MORE = (By.CSS_SELECTOR, ".tm-article-snippet__readmoreeeee")
    FILTERS_DROPDOWN = (By.CSS_SELECTOR, ".tm-navigation-dropdown__button")
    FILTER_BY_RATING = (By.XPATH, "//li[contains(text(), 'rating')]")
    POST_BODY = (By.CSS_SELECTOR, ".tm-article-body")
    TAB_HUBS = (By.XPATH, "//a[contains(text(), 'Hubs')]")
    HUBS = (By.CSS_SELECTOR, ".tm-hubs-list")
    TAB_HUBS_AND_COMPANIES = (By.XPATH, "//h3[contains(text(), 'Hubs')]")

    @allure.step
    def open(self, path=""):
        self._open(self.URL + path)

    @allure.step("Ввожу '{request}' в поисковую строку")
    def search(self, request):
        self.input_and_submit(self.SEARCH_FILED, request)

    @allure.step("Перехожу во вкладку 'Read More'")
    def read_more(self):
        self.click(self.READ_MORE)

    @allure.step("Нажимаю на иконку поиска")
    def click_search(self):
        self.click(self.SEARCH_ICON)

    @allure.step("Выбираю раздел 'Hubs'")
    def select_hubs(self):
        self.click(self.TAB_HUBS)

    @allure.step("Фильтрую результаты поиска по рейтингу")
    def filter_by_rating(self):
        self.click(self.FILTERS_DROPDOWN)
        self.click(self.FILTER_BY_RATING)
