from page_objects import Habr


def test_post_open(remote_browser):
    page = Habr(remote_browser) \
        .open() \
        .click_search() \
        .search('Swift')
    page.filter_by_rating()
    page.read_more()
    page.is_present(page.POST_BODY)


def test_hubs_open(remote_browser):
    page = Habr(remote_browser) \
        .open() \
        .click_search() \
        .search('Dart')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)


def test_post_open_2(remote_browser):
    page = Habr(remote_browser) \
        .open() \
        .click_search() \
        .search('Python')
    page.filter_by_rating()
    page.read_more()
    page.is_present(page.POST_BODY)


def test_hubs_open_2(remote_browser):
    page = Habr(remote_browser) \
        .open() \
        .click_search() \
        .search('Java')
    page.select_hubs_and_companies()
    page.is_present(page.HUBS)
