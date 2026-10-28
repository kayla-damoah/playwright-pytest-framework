from __future__ import annotations

import os

import pytest

from framework.api_client import ApiClient

API_BASE_URL = os.environ.get("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def api() -> ApiClient:
    return ApiClient(API_BASE_URL)
