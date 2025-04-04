import pytest


@pytest.fixture(scope="session")
def monkeysession():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


def pytest_collection_modifyitems(items):
    for item in items:
        if item.location[0].startswith('tests/unit_tests/'):
            item.add_marker('unit')
        elif item.location[0].startswith('tests/integration_tests/'):
            item.add_marker('integration')
        else:
            item.add_marker('other')
