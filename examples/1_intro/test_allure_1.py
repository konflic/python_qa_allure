import pytest
import time


def test_success():
    """this test succeeds"""
    time.sleep(4)
    assert True


def test_failure():
    """this test fails"""
    assert False


def test_skip():
    """this test is skipped"""
    pytest.skip('for a reason!')


def test_broken():
    raise Exception('oops')
