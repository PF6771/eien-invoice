import json
import datetime
import os

DATA_FILE = "eien_data.json"
LOGO_PATH = "eien_logo.png"  # Make sure this file exists in Pythonista
COMPANY_NAME = "AireStream Aire & Heat Co."
COMPANY_ADDRESS = "PO Box 24729\nFort Worth, TX 76124\n817-429-1867"
ZELLE_LINE = "No fees — pay directly with Zelle!"
ZELLE_QR_NOTE = "(Scan Zelle QR code attached)"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_customer(data):
    name = input("Enter customer name: ").strip()
    if name in data:
        print("Customer already exists.")
    else:
        data[name] = {"invoices": []}
        save_data(data)
        print(f"Customer {name} added.")

def format_currency(amount):
    return "${:,.2f}".format(amount)

def create_invoice(data):
    name = input("Customer Name (must match): ").strip()
    if name not in data:
        print("Customer not found.")
        return

    date = input("Invoice Date (YYYY-MM-DD): ").strip()
    po = input("PO Number: ").strip()
    description = input("Description of work/services: ").strip()
    try:
        raw_amount = input("Total Amount ($): ").replace(",", "")
        amount = float(raw_amount)
    except ValueError:
        print("Invalid amount.")
        return
    payment_link = input("Payment Link (or leave blank): ").strip()

    invoice = {
        "date": date,
        "po": po,
        "description": description,
        "amount": amount,
        "paid": 0.0,
        "payment_link": payment_link
    }
    data[name]["invoices"].append(invoice)
    save_data(data)
    print(f"✅ Invoice created for {name}.")

def record_payment(data):
    name = input("Customer Name: ").strip()
    if name not in data:
        print("Customer not found.")
        return

    invoices = [inv for inv in data[name]["invoices"] if inv["paid"] < inv["amount"]]
    if not invoices:
        print("No outstanding invoices.")
        return

    print("\nOutstanding Invoices:")
    for idx, inv in enumerate(invoices):
        balance = inv["amount"] - inv["paid"]
        print(f"{idx + 1}. {inv['date']} | PO: {inv['po']} | Balance: {format_currency(balance)}")

    try:
        choice = int(input("Select invoice number: ")) - 1
        selected = invoices[choice]
    except:
        print("Invalid selection.")
        return

    try:
        raw_payment = input("Enter payment amount: ").replace(",", "")
        payment = float(raw_payment)
    except:
        print("Invalid amount.")
        return

    selected["paid"] += payment
    save_data(data)
    print(f"✅ Payment of {format_currency(payment)} recorded.")

def view_invoices(data, mode="all"):
    name = input("Customer Name: ").strip()
    if name not in data:
        print("Customer not found.")
        return

    invoices = data[name]["invoices"]
    if not invoices:
        print("No invoices.")
        return

    print("\n" + "=" * 40)
    for inv in invoices:
        balance = inv["amount"] - inv["paid"]
        show = (
            (mode == "all") or
            (mode == "paid" and balance <= 0) or
            (mode == "outstanding" and balance > 0)
        )
        if show:
            print(f"Date: {inv['date']}")
            print(f"PO #: {inv['po']}")
            print(f"Description: {inv['description']}")
            print(f"Amount: {format_currency(inv['amount'])}")
            print(f"Paid: {format_currency(inv['paid'])}")
            print(f"Balance: {format_currency(balance)}")
            if inv['payment_link']:
                print(f"Payment Link: {inv['payment_link']}")
            print(f"{ZELLE_LINE}")
            print(f"{ZELLE_QR_NOTE}")
            print("-" * 40)

def main():
    data = load_data()

    while True:
        print("\n=== EIEN MOBILE INVOICING ===")
        print("1. Add Customer")
        print("2. Create Invoice")
        print("3. Record Payment")
        print("4. View Outstanding Invoices")
        print("5. View Paid Invoices")
        print("6. View All Invoices")
        print("7. Exit")

        choice = input("Select option: ").strip()
        if choice == "1":
            add_customer(data)
        elif choice == "2":
            create_invoice(data)
        elif choice == "3":
            record_payment(data)
        elif choice == "4":
            view_invoices(data, "outstanding")
        elif choice == "5":
            view_invoices(data, "paid")
        elif choice == "6":
            view_invoices(data, "all")
        elif choice == "7":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
