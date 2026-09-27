import re
from playwright.sync_api import Page, expect


def login(page: Page):
    """Helper function to handle login"""
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()


def test_loan_applications(page: Page) -> None:
    """Test Case: Multiple Loan Request Workflow"""
    login(page)
    
    def request_loan(amount: str, down_payment: str):
        page.get_by_role("link", name="Request Loan").click()
        page.locator("#amount").fill(amount)
        page.locator("#downPayment").fill(down_payment)
        page.get_by_role("button", name="Apply Now").click()

    # Request Large Loan
    request_loan("50000", "20000")
    
    # Request Small Loan
    request_loan("10000", "5000")