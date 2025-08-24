import json
import os
from datetime import datetime
from collections import defaultdict

# File where expenses will be stored
FILE_NAME = "expenses.json"


# ---------------------- File Handling ----------------------
def load_expenses():
    """Load expenses from JSON file if it exists."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_expenses(expenses):
    """Save expenses to JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------------------- Core Functions ----------------------
def add_expense(expenses):
    """Add a new expense entry."""
    try:
        amount = float(input("Enter amount spent: "))
        category = input("Enter category (Food, Transport, Entertainment, etc.): ").capitalize()
        date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")

        if date_input.strip() == "":
            date = datetime.today().strftime("%Y-%m-%d")
        else:
            date = date_input

        expense = {"amount": amount, "category": category, "date": date}
        expenses.append(expense)
        save_expenses(expenses)
        print("✅ Expense added successfully!\n")
    except ValueError:
        print("❌ Invalid input. Please enter numeric values for amount.\n")


def view_summary(expenses):
    """Display summaries of expenses."""
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    print("\n---- Expense Summary ----")
    print("1. Total Spending")
    print("2. Spending by Category")
    print("3. Spending over Time (daily/monthly)")
    choice = input("Choose an option: ")

    if choice == "1":
        total = sum(exp["amount"] for exp in expenses)
        print(f"\n💰 Total Spending: ${total:.2f}\n")

    elif choice == "2":
        category_totals = defaultdict(float)
        for exp in expenses:
            category_totals[exp["category"]] += exp["amount"]

        print("\n📊 Spending by Category:")
        for cat, total in category_totals.items():
            print(f"{cat}: ${total:.2f}")
        print()

    elif choice == "3":
        time_choice = input("View by (daily/monthly): ").lower()
        time_totals = defaultdict(float)

        for exp in expenses:
            if time_choice == "daily":
                key = exp["date"]
            elif time_choice == "monthly":
                key = exp["date"][:7]  # YYYY-MM
            else:
                print("❌ Invalid choice.")
                return
            time_totals[key] += exp["amount"]

        print(f"\n📆 Spending ({time_choice.capitalize()}):")
        for date, total in time_totals.items():
            print(f"{date}: ${total:.2f}")
        print()
    else:
        print("❌ Invalid option.\n")


def delete_expense(expenses):
    """Delete an expense by index."""
    if not expenses:
        print("No expenses to delete.\n")
        return

    print("\n---- Expenses List ----")
    for idx, exp in enumerate(expenses, start=1):
        print(f"{idx}. {exp['date']} | {exp['category']} | ${exp['amount']:.2f}")

    try:
        choice = int(input("\nEnter the expense number to delete: "))
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            save_expenses(expenses)
            print(f"🗑️ Deleted: {removed}")
        else:
            print("❌ Invalid selection.\n")
    except ValueError:
        print("❌ Please enter a valid number.\n")


# ---------------------- Main Menu ----------------------
def main():
    expenses = load_expenses()

    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Delete Expense (Bonus)")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            print("✅ Exited successfully...!")
            print("🙂 Have a nice day...!")
            break
        else:
            print("❌ Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
