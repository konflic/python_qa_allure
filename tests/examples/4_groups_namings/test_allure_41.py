import allure


@allure.story('Valid credentials')
@allure.feature('Authorization')
@allure.title('Authorization with admin credentials')
def test_with_epic_1():
    pass


@allure.feature('Authorization')
@allure.story('Valid credentials')
@allure.title('Authorization with user credentials')
def test_authorization_user_credentials():
    assert False


@allure.feature('Shopping Cart')
@allure.story('Auth on purchasae')
@allure.title('Авторизация при покупке из корзины')
def test_cart_user_credentials_11():
    raise Exception
