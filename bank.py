from abc import ABC, abstractmethod
from getpass import getpass


class Account(ABC):
    accounts = []
    loans = {}
    bank_balance = 0
    loan_enabled = True

    def __init__(self, name, accountType, email, address):
        self.name = name
        self.accountNo = len(Account.accounts) + 1
        self.balance = 0
        self.accountType = accountType
        self.email = email
        self.address = address
        self.bankrupt = False
        self.transaction_history = []
        Account.accounts.append(self)
        Account.loans[self.accountNo] = 0

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            Account.bank_balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if amount >= 0:
            if self.balance >= amount:
                self.balance -= amount
                Account.bank_balance -= amount
                self.transaction_history.append(f"Withdrew ${amount}")
                print(f"Withdrew ${amount}. New balance: ${self.balance}")
            else:
                print("Withdrawal amount exceeded")
        else:
            print("Invalid withdrawal amount")

    def check_balance(self):
        print(f"Available balance: ${self.balance}")

    def check_transaction_history(self):
        print(f"Transaction history for account {self.accountNo}:")
        for transaction in self.transaction_history:
            print(transaction)

    def request_loan(self, amount):
        if Account.loan_enabled and amount > 0:
            if Account.loans[self.accountNo] < 2:
                Account.loans[self.accountNo] += 1
                self.deposit(amount)
                print(
                    f"Loan approved. You have taken {Account.loans[self.accountNo]} loan(s).")
            else:
                print("You have already taken the maximum number of loans.")
        else:
            print("Loan feature is currently disabled or invalid loan amount")

    def transfer(self, target_account, amount):
        if target_account in Account.accounts:
            if amount >= 0 and self.balance >= amount:
                self.balance -= amount
                target_account.deposit(amount)
                print(
                    f"Transferred ${amount} to account {target_account.accountNo}")
            else:
                print("Invalid transfer amount or insufficient balance")
        else:
            print("Account does not exist")

    @abstractmethod
    def show_info(self):
        pass


class SavingsAccount(Account):
    def show_info(self):
        print(f"Account Type: {self.accountType}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Number: {self.accountNo}")
        print(f"Current Balance: ${self.balance}")


class CurrentAccount(Account):
    def show_info(self):
        print(f"Account Type: {self.accountType}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Number: {self.accountNo}")
        print(f"Current Balance: ${self.balance}")


class AdminAccount(Account):
    def __init__(self, name, email, address, password):
        super().__init__(name, "Admin", email, address)
        self.password = password

    def show_info(self):
        pass


class Admin:

    admin_password = "admin123"  # admin password

    @staticmethod
    def create_account(name, email, address, password):
        if password == Admin.admin_password:
            account = AdminAccount(name, email, address, password)
            print(
                f"Admin account created successfully. Account number is: {account.accountNo}")
        else:
            print("Incorrect admin password. Access denied.")

    @staticmethod
    def delete_account(account_number):
        for account in Account.accounts:
            if account.accountNo == account_number:
                Account.accounts.remove(account)
                del Account.loans[account_number]
                print(f"Account {account_number} has been deleted.")
                return
        print("Account not found.")

    @staticmethod
    def see_all_accounts():
        print("List of all user accounts:")
        for account in Account.accounts:
            print(f"Account No: {account.accountNo}, Name: {account.name}")

    @staticmethod
    def check_bank_balance():
        print(f"Total available balance in the bank: ${Account.bank_balance}")

    @staticmethod
    def check_total_loan_amount():
        total_loans = sum(Account.loans.values())
        print(f"Total loan amount in the bank: ${total_loans}")

    @staticmethod
    def toggle_loan_feature(enable):
        Account.loan_enabled = enable
        status = "enabled" if enable else "disabled"
        print(f"Loan feature is now {status}")


class AccountFactory:
    @staticmethod
    def create_account(name, account_type, email, address):
        account_type = account_type.capitalize()
        if account_type == "Savings":
            return SavingsAccount(name, account_type, email, address)
        elif account_type == "Current":
            return CurrentAccount(name, account_type, email, address)
        else:
            print("Invalid account type")


# Main program
user_account = None
while True:
    print("\nWelcome to the Banking Management System!")
    print("1. User")
    print("2. Admin")
    print("3. Exit")

    choice = input("Select an option (1/2/3): ")

    if choice == "1":
        print("\nUser Menu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Request Loan")
        print("7. Transfer Money")
        print("8. Logout")

        user_choice = input("Select an option: ")

        if user_choice == "1":
            user_name = input("Enter your name: ")
            user_account_type = input(
                "Enter your account type (Savings/Current): ")
            user_account_type = user_account_type.capitalize()
            user_email = input("Enter your email: ")
            user_address = input("Enter your address: ")

            if user_account_type in ["Savings", "Current"]:
                user_account = AccountFactory.create_account(
                    user_name, user_account_type, user_email, user_address)
                print(
                    f"Account created successfully. Your account number is: {user_account.accountNo}")
            else:
                print("Invalid account type")

        elif user_choice == "2":
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter the deposit amount: "))
            for account in Account.accounts:
                if account.accountNo == account_number:
                    account.deposit(amount)
                    break
            else:
                print("Account not found.")

        elif user_choice == "3":
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter the withdrawal amount: "))
            for account in Account.accounts:
                if account.accountNo == account_number:
                    account.withdraw(amount)
                    break
            else:
                print("Account not found.")

        elif user_choice == "4":
            account_number = int(input("Enter your account number: "))
            for account in Account.accounts:
                if account.accountNo == account_number:
                    account.check_balance()
                    break
            else:
                print("Account not found.")

        elif user_choice == "5":
            account_number = int(input("Enter your account number: "))
            for account in Account.accounts:
                if account.accountNo == account_number:
                    account.check_transaction_history()
                    break
            else:
                print("Account not found.")

        elif user_choice == "6":
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter the loan amount: "))
            for account in Account.accounts:
                if account.accountNo == account_number:
                    account.request_loan(amount)
                    break
            else:
                print("Account not found.")

        elif user_choice == "7":
            account_number = int(input("Enter your account number: "))
            target_account_number = int(
                input("Enter the target account number: "))
            amount = float(input("Enter the transfer amount: "))
            user_account = None
            target_account = None
            for account in Account.accounts:
                if account.accountNo == account_number:
                    user_account = account
                elif account.accountNo == target_account_number:
                    target_account = account
            if user_account and target_account:
                user_account.transfer(target_account, amount)
            else:
                print("Account not found.")

        elif user_choice == "8":
            print("Logging out...")
            user_account = None

        else:
            print("Invalid option. Please try again.")

    elif choice == "2":
        print("\nAdmin Menu:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. See All Accounts")
        print("4. Check Bank Balance")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. Toggle Bankrupt")
        print("8. Logout")

        admin_choice = input("Select an option: ")

        if admin_choice == "1":
            admin_name = input("Enter admin name: ")
            admin_email = input("Enter your email: ")
            admin_address = input("Enter your address: ")
            admin_password = getpass("Enter admin password: ")
            Admin.create_account(admin_name, admin_email,
                                 admin_address, admin_password)

        elif admin_choice == "2":
            account_number = int(input("Enter the account number to delete: "))
            Admin.delete_account(account_number)

        elif admin_choice == "3":
            Admin.see_all_accounts()

        elif admin_choice == "4":
            Admin.check_bank_balance()

        elif admin_choice == "5":
            Admin.check_total_loan_amount()

        elif admin_choice == "6":
            enable_loan = input(
                "Enable or disable the loan feature (enable/disable): ")
            if enable_loan == "enable":
                Admin.toggle_loan_feature(True)
            elif enable_loan == "disable":
                Admin.toggle_loan_feature(False)
            else:
                print("Invalid option. Please specify 'enable' or 'disable'.")
        elif admin_choice == "7":
            account_number = bool(
                input("Enter the account number to toggle Bankrupt(True/False): "))
            for account in Account.accounts:
                if account.accountNo == account_number:
                    account.bankrupt = not account.bankrupt
                    status = "Bankrupt" if account.bankrupt else "Not Bankrupt"
                    print(f"Account {account_number} is now {status}.")
                    break
            else:
                print("Account not found.")
                break

        elif admin_choice == "8":
            print("Logging out...")

        else:
            print("Invalid option. Please try again.")

    elif choice == "3":
        print("Exiting the Banking Management System. Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")
