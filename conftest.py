import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "https://httpbin.org"

@pytest.fixture(scope="session")
def session():
    sess = requests.Session()
    yield sess
    sess.close()