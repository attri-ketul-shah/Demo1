
import re
from playwright.sync_api import sync_playwright, expect


BASE_URL = "https://www.saucedemo.com/"


def test_successful_login():

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 1. Open SauceDemo website
            page.goto(BASE_URL)

            # 2. Enter valid username and password
            page.get_by_placeholder("Username").fill("standard_user")
            page.get_by_placeholder("Password").fill("secret_sauce")
            page.wait_for_timeout(3000)
            # 3. Click Login button
            page.get_by_role("button", name="Login").click()

            # 4. Verify successful login
            expect(page).to_have_url(re.compile("inventory.html"))
            expect(page.locator(".title")).to_have_text("Products")
            page.wait_for_timeout(3000)
            print("PASS: Successful login")

        finally:
            browser.close()


def test_invalid_login():

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open website
            page.goto(BASE_URL)

            # Enter invalid credentials
            page.get_by_placeholder("Username").fill("wrong_user")
            page.get_by_placeholder("Password").fill("wrong_password")
            page.wait_for_timeout(3000)
            # Click Login
            page.get_by_role("button", name="Login").click()

            # Verify error message
            error = page.locator('[data-test="error"]')

            expect(error).to_contain_text(
                "Username and password do not match"
            )

            print("PASS: Invalid login validation")

        finally:
            browser.close()


def test_empty_username():

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open website
            page.goto(BASE_URL)

            # Enter password only
            page.get_by_placeholder("Password").fill("secret_sauce")

            # Click Login
            page.get_by_role("button", name="Login").click()
            page.wait_for_timeout(3000)
            # Verify username validation
            error = page.locator('[data-test="error"]')

            expect(error).to_contain_text("Username is required")

            print("PASS: Empty username validation")

        finally:
            browser.close()


def test_empty_password():

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open website
            page.goto(BASE_URL)

            # Enter username only
            page.get_by_placeholder("Username").fill("standard_user")
            page.wait_for_timeout(3000)
            # Click Login
            page.get_by_role("button", name="Login").click()
            page.wait_for_timeout(3000)
            # Verify password validation
            error = page.locator('[data-test="error"]')

            expect(error).to_contain_text("Password is required")

            print("PASS: Empty password validation")
            page.wait_for_timeout(2000)
        finally:
            browser.close()


def test_logout():

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open website
            page.goto(BASE_URL)

            # Login with valid credentials
            page.get_by_placeholder("Username").fill("standard_user")
            page.get_by_placeholder("Password").fill("secret_sauce")
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Login").click()

            # Verify login
            expect(page).to_have_url(re.compile("inventory.html"))

            # Browser interaction method 1: Hover
            page.locator("#react-burger-menu-btn").hover()

            # Browser interaction method 2: Click
            page.locator("#react-burger-menu-btn").click()

            # Verify logout link
            logout_link = page.locator("#logout_sidebar_link")
            expect(logout_link).to_be_visible()

            # Browser interaction method 3: Click logout
            logout_link.click()
            page.wait_for_timeout(3000)
            # Browser interaction method 4: Keyboard interaction
            page.keyboard.press("Tab")

            # Verify return to login page
            expect(page).to_have_url(BASE_URL)

            expect(
                page.get_by_placeholder("Username")
            ).to_be_visible()

            expect(
                page.get_by_placeholder("Password")
            ).to_be_visible()

            print("PASS: Logout and return to login page")

        finally:
            browser.close()


if __name__ == "__main__":

    pytest_args = [
        "test_successful_login",
        "test_invalid_login",
        "test_empty_username",
        "test_empty_password",
        "test_logout"
    ]

    print("SauceDemo Login Automation Test Cases")
