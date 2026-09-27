class OpenAccountPage:

    def __init__(self, page):
        self.page = page

    def open_new_savings_account(self, from_account):
        self.page.click("text=Open New Account")
        self.page.select_option("#type", label="SAVINGS")
        self.page.select_option("#fromAccountId", value=from_account)
        self.page.click("input[value='Open New Account']")

        return self.page.locator("#newAccountId").text_content().strip()


class TransferFundsPage:

    def __init__(self, page):
        self.page = page

    def transfer(self, amount, from_account, to_account):
        self.page.click("text=Transfer Funds")
        self.page.fill("#amount", amount)
        self.page.select_option("#fromAccountId", value=from_account)
        self.page.select_option("#toAccountId", value=to_account)
        self.page.click("input[value='Transfer']")

        return self.page.locator("#showResult").text_content()