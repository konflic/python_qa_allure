import pytest
import allure

def step_inside_test_body():
    assert 1 == 1

@allure.step("Class scope")
def class_scope_step():
    pass

@allure.step
def session_scope_step():
    pass


@pytest.fixture(params=[True, False], ids=['param_true', 'param_false'])
def function_scope_fixture_with_finalizer(request):
    if request.param:
        print('True')
    else:
        print('False')

    def function_scope_finalizer():
        print('FINALIZE!')

    request.addfinalizer(function_scope_finalizer)


@pytest.fixture(scope='class')
def class_scope_fixture_with_finalizer(request):
    def class_finalizer_fixture():
        class_scope_step()

    request.addfinalizer(class_finalizer_fixture)


@pytest.fixture(scope='module')
def module_scope_fixture_with_finalizer(request):
    def module_finalizer_fixture():
        print("MODULE!")

    request.addfinalizer(module_finalizer_fixture)


@pytest.fixture(scope='session')
def session_scope_fixture_with_finalizer(request):
    def session_finalizer_fixture():
        session_scope_step()

    request.addfinalizer(session_finalizer_fixture)


class TestClass(object):

    def test_with_scoped_finalizers(self,
                                    function_scope_fixture_with_finalizer,
                                    class_scope_fixture_with_finalizer,
                                    module_scope_fixture_with_finalizer,
                                    session_scope_fixture_with_finalizer):
        step_inside_test_body()
