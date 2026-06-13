from main import Account

def main():
    account = Account()
    
    while True:
        print("\n" + "="*40)
        print("     PERSONAL FINANCE TRACKER")
        print("="*40)
        print("1. Deposit")
        print("2. Withdraw")
        print("3. View Statement")
        print("4. Check Balance")
        print("5. Quit")
        print("="*40)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            try:
                amount = float(input("Enter amount to deposit: $"))
                account.deposit(amount)
                print(f"✓ Successfully deposited ${amount:.2f}")
                print(f"  New balance: ${account.balance:.2f}")
            except (ValueError, TypeError) as e:
                print(f"✗ Error: {e}")
        
        elif choice == "2":
            try:
                amount = float(input("Enter amount to withdraw: $"))
                account.withdraw(amount)
                print(f"✓ Successfully withdrew ${amount:.2f}")
                print(f"  New balance: ${account.balance:.2f}")
            except (ValueError, TypeError) as e:
                print(f"✗ Error: {e}")
        
        elif choice == "3":
            print("\n" + "-"*40)
            print("TRANSACTION HISTORY")
            print("-"*40)
            if account.transaction_count == 0:
                print("No transactions yet.")
            else:
                account.get_statement()
            print("-"*40)
        
        elif choice == "4":
            print(f"\n💰 Current balance: ${account.balance:.2f}")
            print(f"📊 Total transactions: {account.transaction_count}")
        
        elif choice == "5":
            print("\n✓ Thank you for using Personal Finance Tracker!")
            print(f"  Final balance: ${account.balance:.2f}")
            print("  Goodbye! 👋\n")
            break
        
        else:
            print("✗ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
