import os

import pytest
from django.test.utils import override_settings

from config.test import TEST_SETTINGS


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    with override_settings(**TEST_SETTINGS):
        yield


def pytest_collection_modifyitems(config, items):
    on_ci = os.environ.get("CI", "") == "true"
    if on_ci or config.getoption("markexpr") != "":
        # On CI, or user passed -m, do not skip
        return

    skip_slow = pytest.mark.skip(reason="Skipping slow tests")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
