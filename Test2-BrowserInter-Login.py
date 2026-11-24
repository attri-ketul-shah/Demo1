
import re
import pytest
from playwright.async_api import async_playwright, expect


BASE_URL = "https://www.saucedemo.com/"


@pytest.mark.asyncio
async def test_valid_login_and_logout():

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open website
        await page.goto(BASE_URL)

        # Login
        await page.get_by_placeholder("Username").fill("standard_user")
        await page.get_by_placeholder("Password").fill("secret_sauce")
        await page.get_by_role("button", name="Login").click()

        # Verify successful login
        await expect(page).to_have_url(re.compile(r"inventory\.html"))
        await expect(page.locator(".title")).to_have_text("Products")

        # Open menu
        await page.locator("#react-burger-menu-btn").click()

        # Verify logout link
        logout_link = page.locator("#logout_sidebar_link")
        await expect(logout_link).to_be_visible()

        # Logout
        await logout_link.click()

        # Verify successful logout
        await expect(page).to_have_url(BASE_URL)
        await expect(
            page.get_by_placeholder("Username")
        ).to_be_visible()

        await browser.close()


@pytest.mark.asyncio
async def test_invalid_login_displays_error():

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open website
        await page.goto(BASE_URL)

        # Enter invalid credentials
        await page.get_by_placeholder("Username").fill("wrong_user")
        await page.get_by_placeholder("Password").fill("wrong_password")

        # Click login
        await page.get_by_role("button", name="Login").click()

        # Verify error message
        error_message = page.locator('[data-test="error"]')

        await expect(error_message).to_contain_text(
            "Username and password do not match"
        )

        await browser.close()


@pytest.mark.asyncio
async def test_empty_username_displays_validation_error():

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open website
        await page.goto(BASE_URL)

        # Enter password only
        await page.get_by_placeholder("Password").fill("secret_sauce")

        # Click login
        await page.get_by_role("button", name="Login").click()

        # Verify validation error
        error_message = page.locator('[data-test="error"]')

        await expect(error_message).to_contain_text(
            "Username is required"
        )

        await browser.close()
