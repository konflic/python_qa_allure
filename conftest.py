import pytest
import requests
import allure
import time
import json

from selenium import webdriver


def url_data_exists(url, timeout=15):
    # Waiting for data to be available on given url
    with allure.step(f"Waiting for resource availability {url}"):
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
    parser.addoption("--executor", default="localhost")
    parser.addoption("--bversion", action="store", default="80.0")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--video", action="store_true", default=False)


@pytest.fixture
def remote_browser(request):
    browser = request.config.getoption("--browser")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")
    version = request.config.getoption("--bversion")
    executor_url = f"http://{request.config.getoption('--executor')}:4444/wd/hub"

    caps = {
        "browserName": browser,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": vnc,
            "enableVideo": video,
            "enableLog": logs
        },
        "name": "QAPython",
        "screenResolution": "1280x720x24"
    }

    driver = webdriver.Remote(
        desired_capabilities=caps,
        command_executor=executor_url
    )

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.desired_capabilities),
        attachment_type=allure.attachment_type.JSON)

    def finalizer():
        log_url = f"{executor_url}/logs/{driver.session_id}.log"
        video_url = f"{executor_url}/video/{driver.session_id}.mp4"
        driver.quit()

        if request.node.status == 'failed':
            if logs:
                if url_data_exists(log_url):
                    allure.attach(
                        name="selenoid_log_" + driver.session_id,
                        body=requests.get(log_url).text,
                        attachment_type=allure.attachment_type.TEXT)
            if video:
                if url_data_exists(video_url):
                    allure.attach(
                        body=requests.get(video_url).content,
                        name="video_for_" + driver.session_id,
                        attachment_type=allure.attachment_type.MP4)
        else:
            if video and url_data_exists(video_url): requests.delete(url=video_url)
            if logs and url_data_exists(log_url): requests.delete(url=log_url)

    request.addfinalizer(finalizer)
    return driver


@pytest.fixture
def local_browser(request):
    browser = request.config.getoption("--browser")

    if browser == "chrome": driver = webdriver.Chrome()
    elif browser == "firefox": driver = webdriver.Firefox()
    else: raise ValueError("{} browser not supported".format(browser))

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.desired_capabilities),
        attachment_type=allure.attachment_type.JSON)

    request.addfinalizer(driver.quit)
    return driver
