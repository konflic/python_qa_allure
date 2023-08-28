import logging

import pytest
import allure
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


@pytest.fixture
def driver(request):
    service = ChromeService()
    driver = webdriver.Chrome(service=service)

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities),
        attachment_type=allure.attachment_type.JSON)

    driver.test_name = request.node.name
    driver.log_level = logging.DEBUG

    request.addfinalizer(driver.quit)
    return driver
