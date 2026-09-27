import re
from playwright.sync_api import Page, expect


def test_parabank_accounts_overview(page: Page) -> None:

    # 1. Navigate to ParaBank login page
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.wait_for_load_state("networkidle")
    
    # 2. Log in with valid credentials (update credentials as needed for your test environment)
    page.locator("input[name='username']").fill("john")
    page.locator("input[name='password']").fill("demo")
    page.get_by_role("button", name="Log In").click()
    
    # Verify successful login landing on overview/accounts page
    expect(page.get_by_role("link", name="Log Out")).to_be_visible()
    
    # 3. Click on the Accounts Overview link in the left sidebar[cite: 2]
    page.get_by_role("link", name="Accounts Overview").click()
    
    # 4. Review and assert that the accounts table ("accountTable") displaying account numbers and balances is visible
    accounts_table = page.locator("#accountTable")
    expect(accounts_table).to_be_visible()
    
    # 5. Click on the first specific account number link in the table to view its individual activity ledger
    first_account_link = accounts_table.get_by_role("link").first
    first_account_link.click()
    
    # 6. Assert that the individual account details / activity ledger view has loaded properly
    expect(page.locator("#transactionTable")).to_be_visible()
    
    # 7. Capture a verification snapshot of the account activity ledger
    page.screenshot(path="parabank_accounts_overview_snapshot.png", full_page=True)