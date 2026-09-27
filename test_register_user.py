from playwright.sync_api import Page, expect

BASE_URL = "https://parabank.parasoft.com/parabank"


def test_register_new_user(page: Page) -> None:
    """Test Case: Register a new ParaBank user"""
    page.goto(f"{BASE_URL}/register.htm")

    unique_username = f"user_{__import__('uuid').uuid4().hex[:8]}"
    password = "Password123!"

    page.locator("input[name='customer.firstName']").fill("Test")
    page.locator("input[name='customer.lastName']").fill("User")
    page.locator("input[name='customer.address.street']").fill("123 Test Street")
    page.locator("input[name='customer.address.city']").fill("Test City")
    page.locator("input[name='customer.address.state']").fill("CA")
    page.locator("input[name='customer.address.zipCode']").fill("12345")
    page.locator("input[name='customer.phoneNumber']").fill("5551234567")
    page.locator("input[name='customer.ssn']").fill("123-45-6789")
    page.locator("input[name='customer.username']").fill(unique_username)
    page.locator("input[name='customer.password']").fill(password)
    page.locator("input[name='repeatedPassword']").fill(password)

    page.get_by_role("button", name="Register").click()
    page.wait_for_load_state("networkidle")

    expect(page).to_have_url(f"{BASE_URL}/overview.htm")
    expect(page.get_by_role("link", name="Log Out")).to_be_visible()
    expect(page.get_by_text("Welcome")).to_be_visible()
