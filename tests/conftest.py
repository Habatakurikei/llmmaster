import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_api_client():
    pass


def pytest_addoption(parser):
    parser.addoption(
        "--run-api",
        action="store_true",
        default=False,
        help="Run tests that make actual API calls"
    )
