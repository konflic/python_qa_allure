import pytest
import allure


@pytest.fixture
def function_fixture(request):
    def fin():
        print("Function finalizer")

    request.addfinalizer(fin)


@pytest.fixture(scope="session")
def session_fixture(request):
    def fin():
        print("Session finalizer")
    request.addfinalizer(fin)
