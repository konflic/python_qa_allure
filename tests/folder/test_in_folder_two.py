import pytest
import allure

def test_success():
    """this test succeeds"""
    assert True

@pytest.mark.foo
def test_failure():
    """this test fails"""
    assert False

@pytest.mark.foo2
def test_skip():
    """this test is skipped"""
    pytest.skip('for a reason!')


@pytest.mark.super
@pytest.mark.foo2
def test_broken():
    raise Exception('oops')