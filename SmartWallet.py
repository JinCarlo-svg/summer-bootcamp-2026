import json
import os

FILENAME = "wallet_data.json"

def load_data():
    if not os.path.exists(FILENAME):
        return {"balance": 0.0, "transactions": []}
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"balance": 0.0, "transactions": []}

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

wallet = load_data()

while True:
    print("\n==smart_wallet==")
    print(f"current balance: {wallet['balance']} Dh")
    print("-------------------")
    print("1. Record new income (money received)")
    print("2. Record new expense (money spent)")
    print("3. View statement (history)")
    print("4. Exit")
    
    choice = input("What would you like to do? (1-4): ")
    
    if choice == "1":
        amount = float(input("How much did you receive?: "))
        reason = input("Source? (bonus, salary, gift...): ")
        
        # update balance and add transaction
        wallet["balance"] += amount
        wallet["transactions"].append({"type": "income", "amount": amount, "reason": reason})
        
        save_data(wallet)
        print(f"Great! Added {amount} to your account.")
        
    elif choice == "2":
        amount = float(input("How much did you spend?: "))
        if amount > wallet["balance"]:
            print("Transaction denied! Insufficient funds.")
        else:
            reason = input("What did you spend it on? (restaurant, game, coffee...): ")
            
            # deduct from balance and add transaction
            wallet["balance"] -= amount
            wallet["transactions"].append({"type": "expense", "amount": amount, "reason": reason})
            
            save_data(wallet)
            print(f"Deducted {amount}.. money spent!")
            
    elif choice == "3":
        if not wallet["transactions"]:
            print("Your record is clean, no transactions yet.")
        else:
            print("\n--- Account statement ---")
            for idx, t in enumerate(wallet["transactions"], 1):
                color_sign = "+" if t["type"] == "income" else "-"
                print(f"{idx}. [{t['type']}] {color_sign}{t['amount']} -> Reason: {t['reason']}")
                
    elif choice == "4":
        print("Data saved. Goodbye!")
        break
    else:
        print("Invalid choice, please enter a valid number!")
        import json
