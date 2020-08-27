import pytest

def test_success_():
    """this test succeeds"""
    assert True


def test_failure_():
    """this test fails"""
    assert False


def test_skip_():
    """this test is skipped"""
    pytest.skip('for a reason!')


def test_broken_():
    raise Exception('oops')
