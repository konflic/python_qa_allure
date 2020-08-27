# $ pytest tests.py --allure-features feature2 --allure-stories story2

import allure


def test_without_any_annotations_that_wont_be_executed():
    pass


@allure.story('story')
@allure.feature('epic')
@allure.title('This is tile of the story')
def test_with_epic_1():
    with allure.step("Давайте потестируем"):
        with allure.step("И ещё потестируем"):
            pass


@allure.story('story_1')
def test_with_story_1():
    pass


@allure.story('story_2')
def test_with_story_2():
    pass


@allure.story('story_2')
@allure.feature('feature_2')
def test_with_story_2_and_feature_2():
    pass
