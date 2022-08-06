from fixture.application import Application
import json
import os
import pytest


def load_config(file):
    global target
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file, encoding='utf-8-sig') as f:
        target = json.load(f)
    return target

@pytest.fixture(scope = "session")
def app(request):
    fixture = Application()
    def fin():
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

# def pytest_addoption(parser):
#     # using for set the name of config as --reality and use it for next operations
#     parser.addoption("--reality", action="store", default="config_realitka.json")