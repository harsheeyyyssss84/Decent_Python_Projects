import json

FILE_NAME = "accounts_with_pin.json"


class Account:
    def __init__(self, accno, bal):
        self.accountno = accno
        self.balance = bal

    def debit(self):
        try:
            amount = float(input("Enter Amount you want to Debit: "))

            if amount <= 0:
                print("Amount must be greater than zero!")

            elif amount <= self.balance:
                self.balance -= amount
                print("Debited Successfully!!!")
                print(f"Rs. {amount} was Debited from Account Number: {self.accountno}")
                print("Total Balance =", self.get_balance())

            else:
                print("Not Enough Balance!!!")

        except ValueError:
            print("INVALID INPUT!!! ENTER IN NUMBERS!")

    def credit(self):
        try:
            amount = float(input("Enter Amount you want to Credit: "))

            if amount <= 0:
                print("Amount must be greater than zero!")

            else:
                self.balance += amount
                print("Successfully Credited!!!")
                print(f"Rs. {amount} was Credited to Account Number: {self.accountno}")
                print("Total Balance =", self.get_balance())

        except ValueError:
            print("INVALID INPUT!!! ENTER IN NUMBERS!")

    def get_balance(self):
        return self.balance


# Load existing accounts from the new JSON file.
# If it does not exist yet, start with an empty list.
try:
    with open(FILE_NAME, "r") as file:
        accounts_data = json.load(file)

except (FileNotFoundError, json.JSONDecodeError):
    accounts_data = []


search = input("Enter Account Number to Login: ")

current_acc_data = None

for acc in accounts_data:
    if str(acc["accountno"]) == search:
        current_acc_data = acc
        break


if current_acc_data:
    entered_pin = input("Enter your 4-digit PIN: ")

    if entered_pin != str(current_acc_data.get("pin", "")):
        print("\nIncorrect PIN! Account cannot be opened.")
        exit()

    acc1 = Account(
        current_acc_data["accountno"],
        current_acc_data["balance"]
    )

    print(f"\nWelcome Back! ACCOUNT {acc1.accountno} loaded!")

else:
    print("\nAccount Not Found! Create a new Account!")

    try:
        initial_bal = float(input("Enter Initial Balance: "))

        while initial_bal < 0:
            print("Initial balance cannot be negative.")
            initial_bal = float(input("Enter Initial Balance: "))

    except ValueError:
        print("INVALID INPUT!!! ENTER BALANCE IN NUMBERS!")
        exit()

    pin = input("Create a 4-digit PIN: ")

    while not (pin.isdigit() and len(pin) == 4):
        print("PIN must contain exactly 4 digits.")
        pin = input("Create a 4-digit PIN: ")

    acc1 = Account(search, initial_bal)

    current_acc_data = {
        "accountno": search,
        "balance": initial_bal,
        "pin": pin
    }

    accounts_data.append(current_acc_data)


while True:
    try:
        num = int(input(
            "\nEnter 1 To Debit"
            "\nEnter 2 To Credit"
            "\nEnter 3 To Exit"
            "\nEnter Choice: "
        ))

    except ValueError:
        print("INVALID INPUT! Please enter 1, 2, or 3.")
        continue

    if num == 1:
        acc1.debit()

    elif num == 2:
        acc1.credit()

    elif num == 3:
        print("Total Balance =", acc1.get_balance(), "Rs.")
        break

    else:
        print("INVALID INPUT! Please enter 1, 2, or 3.")

    print("Current Balance:", acc1.get_balance())


# Update the account balance in the list before saving.
for acc in accounts_data:
    if str(acc["accountno"]) == str(acc1.accountno):
        acc["balance"] = acc1.balance


# Creates accounts_with_pin.json on first successful exit.
with open(FILE_NAME, "w") as file:
    json.dump(accounts_data, file, indent=4)

print("\nData Saved Successfully, GOODBYE!!!")