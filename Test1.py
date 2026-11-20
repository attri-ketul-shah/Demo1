from playwright.sync_api import Page, expect


def test_valid_login(page: Page):
    # Step 1: Open SauceDemo website
    page.goto("https://www.saucedemo.com/")

    # Step 2: Enter username
    page.get_by_placeholder("Username").fill("standard_user")
    page.wait_for_timeout(4000)  # Wait for 5 seconds
    # Step 3: Enter password
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.wait_for_timeout(4000)  # Wait for 5 seconds
    # Step 4: Click Login button
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(4000)  # Wait for 5 seconds
    # Step 5: Verify successful login
    expect(page.locator(".title")).to_have_text("Products")
    page.wait_for_timeout(4000)  # Wait for 5 seconds
    # Step 6: Print success message
    print("Login successful!")
    

  