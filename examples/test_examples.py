import allure


@allure.severity("HARD")
def test_one():
    with allure.step("Привет"):
        assert 10 == 10
    with allure.step("Пока"):
        assert 1 != 1
