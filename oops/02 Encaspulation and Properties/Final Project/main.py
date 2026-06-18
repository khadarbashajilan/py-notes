class Account:
    def __init__(self):
        self.__balance = 0
        self.__transactions = []


    @property
    def balance(self):
        """Get the current account balance (read-only)."""
        return self.__balance


    def deposit(self, amount):
        """Deposit money into the account. Validates type and positive value."""
        if not isinstance(amount, (int,float)):
            raise TypeError("Should be Integer Number or Float Type")

        if amount <= 0:
            raise ValueError("Amount should be greater than 0")

        self.__balance += amount
        
        self.__transactions.append({
            "type" : "deposit",
            "amount" : amount,
            "balance_after" : self.__balance
            })

    @property
    def transaction_count(self):
        """Get the number of transactions performed (read-only)."""
        return len(self.__transactions)

    
    def withdraw(self, amount):
        """Withdraw money from the account. Validates type, positive value, and sufficient balance."""
        if not isinstance(amount, (int,float)):
            raise TypeError("Should be Integer Number or Float Type")

        if amount <= 0:
            raise ValueError("Amount should be greater than 0")

        if amount > self.__balance:
           raise ValueError("Amount cant be greater than balance")

        self.__balance -= amount

        self.__transactions.append({
            "type":"withdraw",
            "amount": amount,
            "balance_after" : self.__balance
           })


    def get_statement(self):
        """Print the full transaction history."""
        for t in self.__transactions:
            for k,v in t.items():
                print(f"{k} - {v}")
            print()
