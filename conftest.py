import logging

import pytest
import requests
import allure
import time
import json

from selenium import webdriver


@allure.step("Waiting for resource availability {url}")
def wait_url_data(url, timeout=10):
    while timeout:
        response = requests.get(url)
        if not response.ok:
            time.sleep(1)
            timeout -= 1
        else:
            if 'video' in url:
                return response.content
            else:
                return response.text
    return None


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
    parser.addoption("--executor", default="local")
    parser.addoption("--bversion", action="store", default="95.0")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--video", action="store_true", default=True)


@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities),
        attachment_type=allure.attachment_type.JSON)

    driver.test_name = request.node.name
    driver.log_level = logging.DEBUG

    request.addfinalizer(driver.quit)
    return driver
