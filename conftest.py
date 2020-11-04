import pytest
import requests
import allure
import time
import json

from selenium import webdriver


def url_data_exists(url, timeout=15):
    # Ожидание доступности ресурса по url
    with allure.step("Жду доступности ресура {}"):
        while timeout:
            response = requests.get(url)
            if not response.ok:
                time.sleep(1)
                timeout -= 1
        return timeout


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--executor", default=None)


@pytest.fixture
def remote_browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    executor_url = "http://{}:4444".format(executor)

    # Параметры для селеноида
    caps = {
        "browserName": browser,
        "enableVnc": True,
        "enableVideo": True,
        "enableLog": True,
        "name": "QAPython",
        "screenResolution": "1280x720x24",
    }

    driver = webdriver.Remote(
        desired_capabilities=caps,
        command_executor=executor_url + "/wd/hub"
    )

    driver.maximize_window()

    # Атачим параметры запуска браузера
    allure.attach(
        name=driver.session_id,
        body=str(driver.desired_capabilities),
        attachment_type=allure.attachment_type.JSON
    )

    def finalizer():
        log_url = f"{executor_url}/logs/{driver.session_id}.log"
        video_url = f"{executor_url}/video/{driver.session_id}.mp4"

        driver.quit()

        if request.node.status == 'failed':
            # Если статус теста failed

            if url_data_exists(log_url):
                # Если лог появился, то атачим его к репорту
                allure.attach(
                    name="selenoid_log_" + driver.session_id,
                    body=requests.get(log_url).text,
                    attachment_type=allure.attachment_type.TEXT
                )

            if url_data_exists(video_url):
                # Если видео появилось, то атачим его к репорту
                allure.attach(
                    body=requests.get(video_url).content,
                    name="video_for_" + driver.session_id,
                    attachment_type=allure.attachment_type.MP4
                )
        else:
            # Очищаем тестовые данные в селеноиде
            if url_data_exists(video_url): requests.delete(url=video_url)
            if url_data_exists(log_url): requests.delete(url=log_url)

    request.addfinalizer(finalizer)
    return driver


@pytest.fixture
def local_browser(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError("{} browser not supported".format(browser))
    driver.maximize_window()
    # Атачим параметры запуска браузера
    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.desired_capabilities),
        attachment_type=allure.attachment_type.JSON
    )
    request.addfinalizer(driver.quit)
    return driver
