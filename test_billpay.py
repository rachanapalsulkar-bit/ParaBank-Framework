import re
from playwright.sync_api import Page, expect


def login(page: Page):
    """Helper function to handle login for independent test execution"""
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()


def test_bill_payment(page: Page) -> None:
    """Test Case 1: Bill Payment Workflow"""
    login(page)
    
    page.get_by_role("link", name="Bill Pay").click()
    page.locator("input[name=\"payee.name\"]").fill("Riya")
    page.locator("input[name=\"payee.address.street\"]").fill("ravet")
    page.locator("input[name=\"payee.address.city\"]").fill("Pune")
    page.locator("input[name=\"payee.address.state\"]").fill("Maharashtra")
    page.locator("input[name=\"payee.address.zipCode\"]").fill("412101")
    page.locator("input[name=\"payee.phoneNumber\"]").fill("9371236212")
    page.locator("input[name=\"payee.accountNumber\"]").fill("3455")
    page.locator("input[name=\"verifyAccount\"]").fill("3455")
    
    # Handle dropdown selection dynamically
    account_dropdown = page.locator("select[name='fromAccountId']")
    expect(account_dropdown.locator("option")).not_to_have_count(0, timeout=10000)
    account_dropdown.select_option(index=0)
    
    page.locator("input[name=\"amount\"]").fill("120000")
    page.get_by_role("button", name="Send Payment").click()


