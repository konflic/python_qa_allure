def test_one(function_fixture, session_fixture):
    print("from test_one")


def test_two():
    print("from test_two")


def test_three(session_fixture):
    print("from test_three")


def test_four(function_fixture):
    print("from test_four")
