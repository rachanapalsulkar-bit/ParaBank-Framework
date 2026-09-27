from playwright.sync_api import Page, expect

BASE_URL = "https://parabank.parasoft.com/parabank"
USERNAME = "john"
PASSWORD = "demo"


def login(page: Page):
    """Helper function to log in"""
    page.goto(BASE_URL)
    page.locator("input[name='username']").fill(USERNAME)
    page.locator("input[name='password']").fill(PASSWORD)
    page.locator("input[value='Log In']").click()
    page.wait_for_load_state("networkidle")


def test_open_new_account(page: Page) -> None:
    """Test Case: Open a new Savings Account"""
    login(page)

    # Get initial existing account number
    existing_account = str(page.locator("#accountTable a").first.text_content().strip())
    print(f"Initial Account: {existing_account}")

    # Open New Account
    page.click("text=Open New Account")
    page.select_option("#type", label="SAVINGS")
    page.select_option("#fromAccountId", value=existing_account)

    # Submit open account form
    page.get_by_role("button", name="Open New Account").click()
    page.wait_for_load_state("networkidle")

    # Validate new account creation
    new_account_link = page.locator("#newAccountId")
    expect(new_account_link).to_be_visible()
    new_account_number = str(new_account_link.text_content().strip())
    print(f"New Account Created: {new_account_number}")
    assert len(new_account_number) > 0