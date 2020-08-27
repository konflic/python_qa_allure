import pytest
import requests
import allure
import time

from selenium import webdriver


@allure.step("Жду доступности видео")
def url_data_exists(url):
    # Ждем доступности url
    wait = 15
    while wait > 0:
        r = requests.get(url)
        if r.ok:
            return True
        else:
            time.sleep(1)
            wait -= 1
    return False


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# Это какая-то магия отсюда
# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")

    executor_url = "http://192.168.1.70:4444"

    caps = {
        "browserName": browser,
        "enableVnc": True,
        "enableVideo": True,
        "enableLog": True,
        "name": "QAPython",
        "screenResolution": "1280x720x24",
    }

    driver = webdriver.Remote(desired_capabilities=caps,
                              command_executor=executor_url + "/wd/hub")

    driver.maximize_window()

    session_id = driver.session_id

    allure.attach(name=session_id,
                  body=str(driver.desired_capabilities),
                  attachment_type=allure.attachment_type.JSON)

    def fin():
        log_url = executor_url + f"/logs/{session_id}.log"
        video_url = executor_url + f"/video/{session_id}.mp4"

        driver.quit()

        # Проверяем статус теста
        if request.node.status == 'failed':
            if url_data_exists(log_url):
                r = requests.get(log_url)
                allure.attach(name="selenoid_log_" + session_id, body=r.text,
                              attachment_type=allure.attachment_type.TEXT)

            if url_data_exists(video_url):
                allure.attach(body=requests.get(video_url).content,
                              name="video_for_" + session_id,
                              attachment_type=allure.attachment_type.MP4)

        else:
            if url_data_exists(video_url): requests.delete(url=video_url)
            if url_data_exists(log_url): requests.delete(url=log_url)

    request.addfinalizer(fin)
    return driver
