import random
from playwright.sync_api import Page, expect

BASE_URL = "https://parabank.parasoft.com/parabank"
USERNAME = "john"
PASSWORD = "demo"
TRANSFER_AMOUNT = "100"


def login(page: Page):
    """Helper function to log in"""
    page.goto(BASE_URL)
    page.locator("input[name='username']").fill(USERNAME)
    page.locator("input[name='password']").fill(PASSWORD)
    page.locator("input[value='Log In']").click()
    page.wait_for_load_state("networkidle")


def test_transfer_funds(page: Page) -> None:
    """Test Case: Transfer Funds Between Accounts"""
    login(page)

    # Transfer Funds Workflow
    page.click("text=Transfer Funds")
    page.fill("#amount", TRANSFER_AMOUNT)

    # Wait explicitly for AJAX to populate options in both dropdowns
    page.wait_for_function("document.querySelectorAll('#fromAccountId option').length > 0", timeout=15000)
    page.wait_for_function("document.querySelectorAll('#toAccountId option').length > 0", timeout=15000)

    # Extract all available options safely as strings
    from_options = page.locator("#fromAccountId option").evaluate_all(
        "options => options.map(opt => String(opt.value))"
    )
    to_options = page.locator("#toAccountId option").evaluate_all(
        "options => options.map(opt => String(opt.value))"
    )

    # Pick source and destination accounts safely
    selected_from_account = str(from_options[0])
    valid_to_options = [opt for opt in to_options if opt != selected_from_account]
    selected_to_account = str(valid_to_options[0]) if valid_to_options else to_options[0]

    print(f"Transferring funds FROM account: {selected_from_account} TO account: {selected_to_account}")

    # Perform selections and submit transfer
    page.select_option("#fromAccountId", value=selected_from_account)
    page.select_option("#toAccountId", value=selected_to_account)
    page.get_by_role("button", name="TRANSFER").click()

    page.wait_for_load_state("networkidle")

    # Validate success message
    success_message = page.locator("#showResult").text_content()
    assert "Transfer Complete!" in success_message
    print("Funds transferred successfully!")