import logging

import pytest
import time
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def test_success():
    """this test succeeds"""
    time.sleep(1)
    assert False


def test_failure():
    """this test fails"""
    assert random.choice([0, 1]) # -> AssertionError


def test_failure2():
    """this test fails"""
    assert 0  # -> AssertionError


def test_skip():
    """this test is skipped"""
    # pytest.skip('for a reason!')
    pytest.fail('FAIL!')


def test_broken():
    raise Exception('oops')


def test_broken2():
    a = []
    assert a[1]

def test_print():
    print("This is print")
    logger.warning("This is logger!")
