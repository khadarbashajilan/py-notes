class BankAccount:
    bank_name = "Python Savings Bank"
    total_accounts_created = 0
    minimum_balance = 100
    _next_account_number = 1000  # Private class attribute
    _used_numbers = set()  # Track all used numbers

    def __init__(self, name, balance, account_number):
        """Initialize a bank account.

        Note: This constructor is private-ish. Use class methods to create accounts.

        Args:
            name: Account holder's name.
            balance: Initial balance (will be converted to float).
            account_number: Unique account identifier.
        """
        self.account_holder = name
        self.balance = float(balance)
        self.account_number = account_number
        BankAccount.total_accounts_created += 1
        BankAccount._used_numbers.add(account_number)
    
    @classmethod
    def _get_next_number(cls):
        """Private helper to get the next available account number.

        Uses @classmethod because it needs access to class-level tracking
        attributes (_next_account_number, _used_numbers).

        Scans for gaps in used numbers to fill them before incrementing.

        Returns:
            The next available unused account number.
        """
        while cls._next_account_number in cls._used_numbers:
            cls._next_account_number += 1
        current = cls._next_account_number
        cls._next_account_number += 1
        return current
    
    @classmethod
    def create_account(cls, name, balance):
        """Create a new account with auto-assigned number.

        Uses @classmethod because it creates and returns a new instance
        using class-level account numbering logic.

        Args:
            name: Account holder's name.
            balance: Initial balance.

        Returns:
            A new BankAccount instance.
        """
        acc_num = cls._get_next_number()
        return cls(name, balance, acc_num)
    
    @classmethod
    def from_string(cls, account_str):
        """Create an account from 'Name-Balance' string with auto number.

        Uses @classmethod because it acts as an alternative constructor
        that delegates to create_account for instance creation.

        Args:
            account_str: String in format 'Name-Balance' (e.g. 'Alice-500.0').

        Returns:
            A new BankAccount instance.

        Raises:
            ValueError: If format is invalid or balance is not a valid number.
        """
        parts = account_str.split('-')
        if len(parts) != 2:
            raise ValueError("Expected format: 'Name-Balance'")
        name, balance = parts
        try:
            balance_float = float(balance)
        except ValueError:
            raise ValueError("Balance must be a valid number")
        return cls.create_account(name.strip(), balance_float)
    
    @staticmethod
    def is_valid_balance(balance):
        """Check if balance meets minimum requirement.

        Uses @staticmethod because it only uses the class constant
        minimum_balance directly — no instance (self) or class (cls) reference needed.

        Args:
            balance: The balance to check.

        Returns:
            True if balance >= minimum_balance, False otherwise.
        """
        return BankAccount.minimum_balance <= balance

    @classmethod
    def get_bank_info(cls):
        """Return bank info.

        Uses @classmethod because it needs access to class-level attributes
        (bank_name, total_accounts_created) but doesn't need an instance.

        Returns:
            A formatted string with bank name and total account count.
        """
        return f"{cls.bank_name} has {cls.total_accounts_created} accounts"

    def get_balance_info(self):
        """Return detailed account info.

        Uses a regular instance method because it needs instance attributes
        (account_holder, balance, account_number).

        Returns:
            Formatted string with holder name, balance, and account number.
        """
        return f"Account Holder: {self.account_holder}\nBalance: ${self.balance:.2f}\nAccount Number: #{self.account_number}"

    def deposit(self, amount):
        """Deposit money.

        Uses a regular instance method because it modifies instance state (balance).

        Args:
            amount: Positive amount to deposit.

        Returns:
            Success message with deposited amount and new balance.

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        """Withdraw money.

        Uses a regular instance method because it modifies instance state (balance).

        Args:
            amount: Amount to withdraw.

        Returns:
            Success message with withdrawn amount and new balance.

        Raises:
            ValueError: If amount exceeds balance or would breach minimum balance.
        """
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        if not BankAccount.is_valid_balance(self.balance - amount):
            raise ValueError(f"Withdrawal would leave ${self.balance - amount:.2f} (below ${BankAccount.minimum_balance} minimum)")
        self.balance -= amount
        return f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"

    def __str__(self):
        """Return a readable string representation of the account.

        Returns:
            String in format 'Account #<number>: <name> ($<balance>)'.
        """
        return f"Account #{self.account_number}: {self.account_holder} (${self.balance:.2f})"


# Comprehensive test
if __name__ == "__main__":
    # Reset for clean test
    BankAccount.total_accounts_created = 0
    BankAccount._next_account_number = 1000
    BankAccount._used_numbers.clear()
    
    print("=" * 50)
    print("TESTING DIFFERENT CREATION METHODS")
    print("=" * 50)
    
    # Method 1: create_account (auto-number)
    print("\n1. Using create_account() - Auto number:")
    alice = BankAccount.create_account("Alice", 500)
    print(f"   {alice}")
    
    # Method 2: from_string (auto-number)
    print("\n2. Using from_string() - Auto number:")
    bob = BankAccount.from_string("Bob-750.25")
    print(f"   {bob}")
    
    # Method 3: More auto numbers (should fill gaps)
    print("\n3. More auto accounts (should get 1002, 1003, etc.):")
    diana = BankAccount.create_account("Diana", 300)
    print(f"   {diana}")
    eve = BankAccount.from_string("Eve-425")
    print(f"   {eve}")
    
    print("\n" + "=" * 50)
    print("TESTING VALIDATION")
    print("=" * 50)
    
    # Test minimum balance validation
    print("\nTesting minimum balance validation:")
    print(f"   Is balance $50 valid? {BankAccount.is_valid_balance(50)}")
    print(f"   Is balance $100 valid? {BankAccount.is_valid_balance(100)}")
    print(f"   Is balance $150 valid? {BankAccount.is_valid_balance(150)}")
    
    print("\n" + "=" * 50)
    print("TESTING OPERATIONS")
    print("=" * 50)
    
    # Test deposit
    print("\nDeposit test:")
    print(f"   Before: {alice}")
    alice.deposit(200)
    print(f"   After deposit: {alice}")
    
    # Test withdrawal
    print("\nWithdrawal test:")
    print(f"   Before: {bob}")
    try:
        bob.withdraw(700)
        print(f"   After withdraw: {bob}")
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Test minimum balance withdrawal protection
    print("\nMinimum balance protection test:")
    minimal = BankAccount.create_account("Minimal", 100)
    print(f"   Account with exactly $100: {minimal}")
    try:
        minimal.withdraw(1)
        print(f"   ERROR: Should not allow this!")
    except ValueError as e:
        print(f"   ✓ Correctly prevented: {e}")
    
    # Test bank info
    print("\n" + "=" * 50)
    print("BANK SUMMARY")
    print("=" * 50)
    print(f"   {BankAccount.get_bank_info()}")
    print(f"   Next available number: {BankAccount._next_account_number}")
    print(f"   All account numbers: {sorted(BankAccount._used_numbers)}")
    
    print("\n" + "=" * 50)
    print("FINAL ACCOUNT STATUS")
    print("=" * 50)
    for acc in [alice, bob, diana, eve]:
        print(f"   {acc.get_balance_info()}")

# ============================================================
# Concept: @classmethod vs @staticmethod vs Instance Methods
# ============================================================
# Instance methods (def method(self, ...)) operate on instance
# data and need self. Class methods (@classmethod, def method(cls, ...))
# receive the class as first argument and are used for factory
# methods or class-level logic. Static methods (@staticmethod,
# def method(...)) receive no special first argument and behave
# like plain functions grouped inside the class for organization.
#
# Key Terminology:
#   - @classmethod:  Method bound to the class, not the instance
#                    (receives cls as first argument)
#   - @staticmethod: Method that does not receive self or cls;
#                    acts like a regular function in the class
#   - Instance Method: Regular method that receives self and
#                      operates on instance attributes
#   - Factory Method: A class method that creates & returns
#                     instances (e.g., create_account, from_string)
#   - Class Attribute: Shared across all instances (e.g., bank_name)
#   - Private Convention: Prefix _ indicates internal use (e.g.,
#                         _next_account_number)
# ============================================================"
