
from pathlib import Path
from playwright.sync_api import Page, expect


# Read credentials from TXT file
CREDENTIAL_FILE = Path(
    r"D:\GitHub-Learning\Demo1\credentials.txt"
)

with open(CREDENTIAL_FILE, "r") as file:
    username = file.readline().strip()
    password = file.readline().strip()


def test_successful_login(page: Page):

    # Open SauceDemo website
    page.goto("https://www.saucedemo.com/")

    # Assertion 1: Verify page title
    expect(page).to_have_title("Swag Labs")

    # Enter valid credentials from TXT file
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)

    # Click login button
    page.locator("#login-button").click()
    page.wait_for_timeout(2000)
    # Assertion 2: Verify successful login URL
    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # Assertion 3: Verify Products heading
    expect(page.locator(".title")).to_have_text("Products")

    # Assertion 4: Verify product visibility
    expect(
        page.get_by_text("Sauce Labs Backpack")
    ).to_be_visible()

    # Assertion 5: Verify shopping cart visibility
    expect(
        page.locator(".shopping_cart_link")
    ).to_be_visible()


def test_invalid_login(page: Page):

    # Open SauceDemo website
    page.goto("https://www.saucedemo.com/")

    # Use invalid credentials
    invalid_username = "wrong_user"
    invalid_password = "wrong_password"

    page.locator("#user-name").fill(invalid_username)
    page.locator("#password").fill(invalid_password)

    # Click login button
    page.locator("#login-button").click()
    page.wait_for_timeout(2000)
    # Assertion 6: Verify invalid login error
    expect(
        page.locator('[data-test="error"]')
    ).to_contain_text(
        "Username and password do not match"
    )

    # Assertion 7: Verify user remains on login page
    expect(page).to_have_url(
        "https://www.saucedemo.com/"
    )


