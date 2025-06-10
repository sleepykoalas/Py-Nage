import sys
import os
import hashlib
import getpass

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def verify_pass(entered, stored):
    salt_hex, hash_hex = stored.strip().split(":")
    salt = bytes.fromhex(salt_hex)
    stored_hash = bytes.fromhex(hash_hex)
    check_hash = hashlib.pbkdf2_hmac('sha256', entered.encode(), salt, 100_000)
    return check_hash == stored_hash

def password_check():
    with open("password.txt", "r") as file:
        stored_hash = file.read()
    while True:
        password = getpass.getpass("Enter Master Password: ")
        clear()
        if verify_pass(password, stored_hash):
            print("Access Granted. Loading...")
            clear()
            stockmanage()
            break
        else:
            print("Password Invalid")
            input("Press Enter to try again...")
            clear()

def sell_product():
    product_to_sell = input("Enter the exact product model to remove: ").strip().lower()
    found = False
    with open("stock.txt", "r") as file:
        lines = file.readlines()

    with open("stock.txt", "w") as file:
        for line in lines:
            line_stripped = line.strip().lower()
            if line_stripped.startswith(f"product: {product_to_sell},"):
                found = True
                continue
            file.write(line)

    if found:
        input("Product removed successfully. Press Enter to continue...")
    else:
        input("Product not found. Press Enter to return...")
    clear()

def stockmanage():
    help_msg = """
Commands for Py-Nage Stock Management:

  'buy'     - Add a product to stock.
  'sell'    - Remove a product from stock.
  'help'    - Display this message.
  'credits' - Show credits for the program.
  'exit'    - Exit the program.
  'leave'   - Exit the program.
  'view'    - View current stock.
"""
    while True:
        whattodo = input(">> ").strip().lower()
        if whattodo in ["exit", "leave"]:
            print("Exiting...")
            sys.exit(0)
        elif whattodo == "buy":
            nameofproductadd = input("Product Model: ")
            typeofadd = input("Product Category: ")
            quantitytoadd = input("Quantity: ")
            remarksadd = input("Remarks (leave blank for none): ")
            with open("stock.txt", "a") as file:
                file.write(f"\nProduct: {nameofproductadd},Category: {typeofadd},Amount: {quantitytoadd},Remarks: {remarksadd}")
            input("Successfully Added to Stock! Press Enter to return: ")
            clear()
        elif whattodo == "sell":
            clear()
            sell_product()
        elif whattodo == "help":
            clear()
            print(help_msg)
            input("Press Enter to continue...")
            clear()
        elif whattodo == "credits":
            clear()
            print("Py-Nage Stock Management System\nCreated by Kim Pirun\nVersion 1.0\nThanks to the Chompy family and CMUA!")
            input("Press Enter to continue...")
            clear()
        elif whattodo == "view":
            clear()
            if os.path.getsize("stock.txt") == 0:
                print("No stock available.")
            else:
                with open("stock.txt", "r") as file:
                    stock_data = file.read()
                    print("Current Stock:\n" + stock_data)
            input("Press Enter to continue...")
            clear()
        else:
            input("Unknown command. Type 'help' for commands.")
            clear()

def hash_pass(text):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', text.encode(), salt, 100_000)
    return f"{salt.hex()}:{hashed.hex()}"

def startup_check():
    passfile = "password.txt"
    stockfile = "stock.txt"

    if not os.path.exists(passfile):
        open(passfile, "w").close()
    if os.path.getsize(passfile) == 0:
        while True:
            password = getpass.getpass("Welcome to Py-Nage! First Load Detected! Enter Master Password: ")
            confirm = getpass.getpass("Confirm Master Password: ")
            clear()
            if password == confirm:
                hashed_pass = hash_pass(password)
                with open(passfile, "w") as file:
                    file.write(hashed_pass)
                clear()
                print("Master Password Set Successfully!")
                break
            else:
                print("Passwords do not match. Try again.")

    if not os.path.exists(stockfile):
        open(stockfile, "a").close()

    password_check()

if __name__ == "__main__":
    startup_check()
