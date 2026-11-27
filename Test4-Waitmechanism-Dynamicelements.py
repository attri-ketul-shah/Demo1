
from pathlib import Path
from playwright.sync_api import Page, expect


# Read credentials from TXT file
CREDENTIAL_FILE = Path(__file__).parent / "credentials.txt.txt"

with open(CREDENTIAL_FILE, "r") as file:
    username = file.readline().strip()
    password = file.readline().strip()


# Test 1: Login waits for Products heading
def test_login_waits_for_products_heading(page: Page):

    # Navigate to SauceDemo
    page.goto("https://www.saucedemo.com/")

    # Enter username and password
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)

    # Click login button
    page.locator("#login-button").click()
    # Locate Products heading
    products_heading = page.locator(".title")

    # Wait until Products heading becomes visible
    products_heading.wait_for(state="visible")

    # Assertion 1: Verify heading is visible
    expect(products_heading).to_be_visible()

    # Assertion 2: Verify heading text
    expect(products_heading).to_have_text("Products")

    # Assertion 3: Verify successful login URL
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Assertion 4: Verify product is visible
    expect(
        page.get_by_text("Sauce Labs Backpack")
    ).to_be_visible()


# Test 2: Diagnostic exercise - Incorrect locator
def test_diagnostic_timeout_failure(page: Page):

    # Navigate to SauceDemo
    page.goto("https://www.saucedemo.com/")

    # Enter valid credentials
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)

    # Click login
    page.locator("#login-button").click()
    page.wait_for_timeout(2000)
    # Intentionally incorrect locator
    incorrect_heading = page.locator(".product-title")

    # Wait for incorrect locator to become visible
    # This will intentionally generate a timeout failure
    incorrect_heading.wait_for(
        state="visible",
        timeout=3000
    )

    # This assertion will not be reached if the wait times out
    expect(incorrect_heading).to_be_visible()


# Test 3: Corrected locator after diagnosing timeout
def test_corrected_products_heading(page: Page):

    # Navigate to SauceDemo
    page.goto("https://www.saucedemo.com/")

    # Enter valid credentials
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)

    # Click login
    page.locator("#login-button").click()
    page.wait_for_timeout(2000)
    # Correct locator
    products_heading = page.locator(".title")

    # Wait until heading becomes visible
    products_heading.wait_for(state="visible")

    # Verify heading
    expect(products_heading).to_be_visible()
    expect(products_heading).to_have_text("Products")
