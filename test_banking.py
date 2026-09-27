import random
from playwright.sync_api import Page

BASE_URL = "https://parabank.parasoft.com/parabank"

USERNAME = "john"
PASSWORD = "demo"

TRANSFER_AMOUNT = "100"


def test_open_account_and_transfer(page: Page) -> None:
    # Login
    page.goto(BASE_URL)
    page.locator("input[name='username']").fill(USERNAME)
    page.locator("input[name='password']").fill(PASSWORD)
    page.locator("input[value='Log In']").click()
    page.wait_for_load_state("networkidle")

    # Get initial existing account number as a string
    existing_account = str(page.locator("#accountTable a").first.text_content().strip())
    print(f"Initial Account: {existing_account}")

    # Open New Account
    page.click("text=Open New Account")
    page.select_option("#type", label="SAVINGS")
    page.select_option("#fromAccountId", value=existing_account)

    # Submit open account form
    page.get_by_role("button", name="Open New Account").click()
    page.wait_for_load_state("networkidle")

    # Capture new account number as a string
    new_account_link = page.locator("#newAccountId")
    new_account_number = str(new_account_link.text_content().strip())
    print(f"New Account Created: {new_account_number}")

    # Transfer Funds Workflow
    page.click("text=Transfer Funds")
    page.fill("#amount", TRANSFER_AMOUNT)

    # Wait explicitly for AJAX to populate options in both dropdowns before reading them
    page.wait_for_function("document.querySelectorAll('#fromAccountId option').length > 0", timeout=15000)
    page.wait_for_function("document.querySelectorAll('#toAccountId option').length > 0", timeout=15000)

    # Extract all available options safely as strings
    from_options = page.locator("#fromAccountId option").evaluate_all(
        "options => options.map(opt => String(opt.value))"
    )
    to_options = page.locator("#toAccountId option").evaluate_all(
        "options => options.map(opt => String(opt.value))"
    )

    # Skip the first option (index 0) to select a different existing account
    skippable_from_options = from_options[1:] if len(from_options) > 1 else from_options

    # Pick a random source account from the skippable options
    selected_from_account = str(random.choice(skippable_from_options)) if skippable_from_options else existing_account

    # Guarantee 'toAccountId' is different from 'fromAccountId'
    valid_to_options = [opt for opt in to_options if opt != selected_from_account]

    if new_account_number in valid_to_options:
        selected_to_account = new_account_number
    elif valid_to_options:
        selected_to_account = random.choice(valid_to_options)
    else:
        selected_to_account = to_options[0]

    print(f"Transferring funds FROM account: {selected_from_account} TO account: {selected_to_account}")

    # Perform explicit string selections
    page.select_option("#fromAccountId", value=selected_from_account)
    page.select_option("#toAccountId", value=selected_to_account)

    # Click Transfer button using its exact uppercase name/role
    page.get_by_role("button", name="TRANSFER").click()

    page.wait_for_load_state("networkidle")

    success_message = page.locator("#showResult").text_content()
    assert "Transfer Complete!" in success_message

    print("Funds transferred successfully!")


