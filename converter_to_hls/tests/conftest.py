import pytest

from main import create_app


@pytest.fixture
def cli(loop, test_client):
    return loop.run_until_complete(test_client(create_app()))
