"""Thin wrapper around requests so tests read as intent, not plumbing."""
from __future__ import annotations

import allure
import requests


class ApiClient:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        with allure.step(f"{method} {path}"):
            return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)
