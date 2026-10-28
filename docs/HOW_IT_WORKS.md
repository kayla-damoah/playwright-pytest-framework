# How it works

This document covers the design of the test suite: how a run flows through the code and why it is structured this way.

## Overview

The suite has two halves. The API tests call a public REST service ([JSONPlaceholder](https://jsonplaceholder.typicode.com)) and check status codes, response shape and behaviour. The UI tests drive a real browser through a public demo shop ([Sauce Demo](https://www.saucedemo.com)): logging in, browsing and sorting products, filling the cart and checking out. Everything runs on GitHub Actions for every push, and the results are published as an [Allure report](https://kayla-damoah.github.io/playwright-pytest-framework/).

| Tool | Role |
|---|---|
| pytest | Discovers and runs tests; fixtures, parametrization and markers |
| Playwright | Controls the browser; auto-waits for elements; provides `expect` assertions and traces |
| requests | HTTP client used by the API tests |
| Allure | Turns results into a browsable report with steps and failure screenshots |
| GitHub Actions | Runs the suite and publishes the report on every push |

## Layers

```
Tests          what is being checked                  tests/
Fixtures       setup shared by tests                  conftest.py files
Page objects   where things are, how to use them      framework/pages/
Playwright     browser control
```

Tests never contain selectors, and page objects never contain test-specific assertions beyond confirming an action took effect.

## Project layout

```
framework/api_client.py      requests wrapper with a step per call
framework/pages/             LoginPage, InventoryPage, CartPage
tests/api/                   REST API tests
tests/ui/                    browser tests
tests/ui/conftest.py         viewport, logged-in session, screenshot on failure
conftest.py                  shared API client fixture
pytest.ini                   markers, Allure and Playwright options
.github/workflows/ci.yml     run tests, build the report, publish to Pages
```

## Anatomy of a UI test

Following `test_end_to_end_checkout_shows_confirmation`:

1. pytest-playwright provides a fresh browser `page` for the test.
2. The `login_page` fixture opens the site. The `inventory` fixture logs in, waits for the product list URL, and hands the test an `InventoryPage`.
3. `add_to_cart(...)` clicks the product's button and waits for it to change to "Remove".
4. `open_cart()` clicks the cart icon, waits for the cart URL, and returns a `CartPage`.
5. `checkout(...)` fills the form, confirms the fields kept their values, continues, and finishes.
6. The test asserts the confirmation message with `expect`.
7. If the test failed, a fixture attaches a screenshot to the report. Playwright also keeps a trace of the failed run.

## Design decisions

- **Page Object Model.** Selectors live in one place per screen, so a UI change is a one-line fix instead of an edit to every test.
- **Playwright's auto-waiting and `expect`.** Locator actions wait for elements to be ready, and `expect(...)` retries until its condition holds or times out. There are no fixed sleeps.
- **Fixtures for setup.** A logged-in `inventory` fixture keeps tests short and removes repeated login code.
- **Markers.** `api`, `ui` and `smoke` select subsets: `pytest -m smoke`.
- **Parametrization.** Invalid-login cases and user-filter cases run from one test function each.
- **An API client wrapper.** `ApiClient` sets a default timeout and records each call as a report step.
- **Strict markers.** `--strict-markers` turns a misspelled marker into an error instead of a silently unselected test.

## Reporting

The `allure-pytest` plugin records every run to `reports/allure-results/`. Page-object methods and API calls are decorated as steps, so each test shows its actions in order, grouped by feature (Login, Inventory, Checkout, Posts API). A fixture attaches a screenshot to failed UI tests. CI generates the report after every run, including failed ones, and publishes it to GitHub Pages from `main`. The Environment panel lists the browser, Python version, OS, targets and commit.

## Known limitations

- Only Chromium is exercised in CI.
- Tests run serially.
- The suite depends on two public demo services, so an outage or change on their side can fail a run.
- The Allure report shows only the latest run; there is no history across runs.
