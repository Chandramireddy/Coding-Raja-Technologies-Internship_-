import datetime

class Transaction:
    def __init__(self, amount, category, transaction_type, date=None):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type  # 'income' or 'expense'
        self.date = date if date else datetime.date.today()

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} - {self.transaction_type.capitalize()} of ${self.amount} in {self.category}"

import pickle

class BudgetTracker:
    def __init__(self, data_file):
        self.transactions = []
        self.data_file = data_file
        self.load_transactions()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self):
        total_income = sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'income')
        total_expenses = sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'expense')
        remaining_budget = total_income - total_expenses
        return total_income, total_expenses, remaining_budget

    def categorize_expenses(self):
        categories = {}
        for transaction in self.transactions:
            if transaction.transaction_type == 'expense':
                if transaction.category in categories:
                    categories[transaction.category] += transaction.amount
                else:
                    categories[transaction.category] = transaction.amount
        return categories

    def list_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def save_transactions(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.transactions, f)

    def load_transactions(self):
        try:
            with open(self.data_file, 'rb') as f:
                self.transactions = pickle.load(f)
        except FileNotFoundError:
            self.transactions = []

    def clear_transactions(self):
        self.transactions = []
        self.save_transactions()

import datetime

def print_menu():
    print("Command Menu:")
    print("  1. Add Income")
    print("  2. Add Expense")
    print("  3. Remaining Budget")
    print("  4. view expenses")
    print("  5. List Transactions")
    print("  6. Exit")
    print()

def get_amount_input(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return amount
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    data_file = "transactions.pickle"  # You can change the filename or path as needed
    budget_tracker = BudgetTracker(data_file)

    while True:
        print_menu()
        choice = input("Enter command number: ").strip()

        if choice == '1':
            amount = get_amount_input("Enter income amount: $")
            category = input("Enter income category: ").strip()
            transaction = Transaction(amount, category, 'income')
            budget_tracker.add_transaction(transaction)
            print("Income added!\n")

        elif choice == '2':
            amount = get_amount_input("Enter expense amount: $")
            category = input("Enter expense category: ").strip()
            transaction = Transaction(amount, category, 'expense')
            budget_tracker.add_transaction(transaction)
            print("Expense added!\n")

        elif choice == '3':
            total_income, total_expenses, remaining_budget = budget_tracker.calculate_budget()
            print(f"Total Income: ${total_income}")
            print(f"Total Expenses: ${total_expenses}")
            print(f"Remaining Budget: ${remaining_budget}\n")

        elif choice == '4':
            categories = budget_tracker.categorize_expenses()
            print("view expenses:")
            for category, amount in categories.items():
                print(f"{category}: ${amount}")
            print()

        elif choice == '5':
            budget_tracker.list_transactions()
            print()

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid command. Please enter a number between 1 and 6.\n")

if __name__ == '__main__':
    main()