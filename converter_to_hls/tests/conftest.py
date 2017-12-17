import pytest

from main import create_app


@pytest.fixture
def cli(loop, test_client):
    app = create_app(loop)
    return loop.run_until_complete(test_client(app))
