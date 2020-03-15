import pytest
import requests
import allure
import time

from selenium import webdriver


def url_data_exists(url):
    # Ждем доступности url
    wait = 10
    while wait > 0:
        r = requests.get(url)
        if r.ok:
            return True
        else:
            time.sleep(1)
            wait -= 1
    return False


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# Это какая-то магия отсюда https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")

    executor_url = "http://localhost:4444"
    caps = {"browserName": browser,
            "enableVnc": True,
            "enableVideo": True,
            "enableLog": True,
            "name": "QAPython"}

    driver = webdriver.Remote(desired_capabilities=caps,
                              command_executor=executor_url + "/wd/hub")

    def fin():
        log_url = executor_url + f"/logs/{driver.session_id}.log"
        video_url = executor_url + f"/video/{driver.session_id}.mp4"

        driver.quit()

        # Проверяем статус
        if request.node.status == 'failed':
            if url_data_exists(video_url):
                allure.attach(body=requests.get(video_url).content,
                              attachment_type=allure.attachment_type.MP4)

            if url_data_exists(log_url):
                r = requests.get(log_url)
                allure.attach(name="selenoid_log", body=r.text,
                              attachment_type=allure.attachment_type.TEXT)
        else:
            # Удаляем данные теста
            if url_data_exists(video_url): requests.delete(url=video_url)
            if url_data_exists(log_url): requests.delete(url=log_url)

    allure.attach(name=driver.session_id,
                  body=str(driver.desired_capabilities),
                  attachment_type=allure.attachment_type.JSON)

    request.addfinalizer(fin)
    return driver
