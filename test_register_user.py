from uuid import uuid4

from playwright.sync_api import Page, expect

BASE_URL = "https://parabank.parasoft.com/parabank"


def fill_registration_form(page: Page, username: str, password: str) -> None:
    page.locator("input[name='customer.firstName']").fill("Test")
    page.locator("input[name='customer.lastName']").fill("User")
    page.locator("input[name='customer.address.street']").fill("123 Test Street")
    page.locator("input[name='customer.address.city']").fill("Test City")
    page.locator("input[name='customer.address.state']").fill("CA")
    page.locator("input[name='customer.address.zipCode']").fill("12345")
    page.locator("input[name='customer.phoneNumber']").fill("5551234567")
    page.locator("input[name='customer.ssn']").fill("123-45-6789")
    page.locator("input[name='customer.username']").fill(username)
    page.locator("input[name='customer.password']").fill(password)
    page.locator("input[name='repeatedPassword']").fill(password)


def test_register_new_user(page: Page) -> None:
    """Test Case: Register a new ParaBank user"""
    page.goto(f"{BASE_URL}/register.htm")

    unique_username = f"user_{uuid4().hex[:8]}"
    password = "Password123!"
    fill_registration_form(page, unique_username, password)

    page.get_by_role("button", name="Register").click()
    page.wait_for_load_state("networkidle")

    expect(page.get_by_role("link", name="Log Out")).to_be_visible()
    expect(page.get_by_text("Your account was created successfully. You are now logged in.")).to_be_visible()
    expect(page.get_by_text(f"Welcome {unique_username}")).to_be_visible()


def test_register_existing_username_is_rejected(page: Page) -> None:
    """Test Case: Reject registration with a username that already exists"""
    page.goto(f"{BASE_URL}/register.htm")

    username = f"user_{uuid4().hex[:8]}"
    password = "Password123!"

    fill_registration_form(page, username, password)
    page.get_by_role("button", name="Register").click()
    expect(page.get_by_text("Your account was created successfully. You are now logged in.")).to_be_visible()

    page.get_by_role("link", name="Log Out").click()
    page.goto(f"{BASE_URL}/register.htm")
    fill_registration_form(page, username, password)
    page.get_by_role("button", name="Register").click()

    expect(page.get_by_text("This username already exists.")).to_be_visible()
    expect(page.get_by_role("link", name="Log Out")).not_to_be_visible()
