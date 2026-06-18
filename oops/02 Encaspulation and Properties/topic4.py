from datetime import datetime
from copy import deepcopy
import sys


class DigitalWallet:
    """Demonstrates private attributes, encapsulated transaction history, and deep copy safety."""

    def __init__(self, userid, username, initial_balance):
        """Initialize wallet with user details and optional initial balance."""
        self.userid = userid
        self.username = username
        self.__balance = 0
        self.__transaction_history = []
        self.__transaction_counter = 0

        if not isinstance(initial_balance, (int, float)):
            raise TypeError("Initial balance must be a number (int or float)")
        if initial_balance < 0:
            raise ValueError("Balance cannot be negative")
        if initial_balance > 0:
            self.deposit(initial_balance)

    def __add_transaction(self, txn_type, amount):
        """Internal helper to build and store a transaction record with a unique ID."""
        self.__transaction_counter += 1
        self.__transaction_history.append({
            'id': self.__transaction_counter,
            'type': txn_type,
            'amount': amount,
            'balance': self.__balance,
            'timestamp': datetime.now()
        })

    def deposit(self, amount):
        """Deposit money into the wallet. Amount must be positive."""
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number (int or float)")

        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.__balance += amount
        self.__add_transaction('Deposit', amount)

        return "Successful Deposit"

    def withdraw(self, amount):
        """Withdraw money from the wallet. Amount must be positive and cannot exceed balance."""
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number (int or float)")

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.__balance:
            raise ValueError("Insufficient balance")

        self.__balance -= amount
        self.__add_transaction('Withdraw', amount)

        return "Successful Withdrawal"

    @property
    def balance(self):
        """Return current balance."""
        return self.__balance

    def get_transaction_history(self):
        """
        Return a copy of the transaction history.
        deepcopy is used so callers cannot mutate the internal history list
        or any of the dicts inside it, preserving data integrity.
        """
        if not self.__transaction_history:
            return "No transactions yet"
        return deepcopy(self.__transaction_history)


def main():
    """Run a set of tests to verify DigitalWallet works correctly."""

    # Test 1: Valid init with initial balance
    w = DigitalWallet("u1", "Alice", 100)
    assert w.balance == 100, "Balance should be 100"
    assert w.userid == "u1"
    assert w.username == "Alice"
    print("Test 1 passed: Valid init with balance")

    # Test 2: Valid init with zero balance — no transaction recorded
    w2 = DigitalWallet("u2", "Bob", 0)
    assert w2.balance == 0
    assert w2.get_transaction_history() == "No transactions yet"
    print("Test 2 passed: Zero balance init")

    # Test 3: Init with negative balance raises ValueError
    try:
        DigitalWallet("u3", "Bad", -50)
        assert False, "Should have raised"
    except ValueError:
        print("Test 3 passed: Negative init rejected")

    # Test 4: Init with non-numeric balance raises TypeError
    try:
        DigitalWallet("u4", "Bad", "lots")
        assert False, "Should have raised"
    except TypeError:
        print("Test 4 passed: Non-numeric init rejected")

    # Test 5: Deposit increases balance and records transaction with amount
    w.deposit(50)
    assert w.balance == 150
    last = w.get_transaction_history()[-1]
    assert last['type'] == 'Deposit'
    assert last['amount'] == 50
    assert last['balance'] == 150
    print("Test 5 passed: Deposit works and records amount")

    # Test 6: Withdraw decreases balance and records transaction
    w.withdraw(30)
    assert w.balance == 120
    last = w.get_transaction_history()[-1]
    assert last['type'] == 'Withdraw'
    assert last['amount'] == 30
    assert last['balance'] == 120
    print("Test 6 passed: Withdraw works and records amount")

    # Test 7: Withdraw more than balance raises ValueError
    try:
        w.withdraw(999)
        assert False, "Should have raised"
    except ValueError:
        print("Test 7 passed: Over-withdraw rejected")

    # Test 8: Deposit/Withdraw of zero or negative raises ValueError
    for invalid in [0, -10]:
        try:
            w.deposit(invalid)
            assert False, "Should have raised"
        except ValueError:
            pass
        try:
            w.withdraw(invalid)
            assert False, "Should have raised"
        except ValueError:
            pass
    print("Test 8 passed: Zero/negative amounts rejected")

    # Test 9: Non-numeric deposit/withdraw raises TypeError
    try:
        w.deposit("abc")
        assert False
    except TypeError:
        pass
    try:
        w.withdraw([1, 2])
        assert False
    except TypeError:
        pass
    print("Test 9 passed: Non-numeric amounts rejected")

    # Test 10: Transaction history uses deepcopy — mutating the copy doesn't affect internal state
    hist = w.get_transaction_history()
    hist.clear()
    assert len(w.get_transaction_history()) > 0, "Internal history should be untouched"
    print("Test 10 passed: deepcopy protects internal history")

    # Test 11: Transaction records contain all required fields
    for txn in w.get_transaction_history():
        for key in ('id', 'type', 'amount', 'balance', 'timestamp'):
            assert key in txn, f"Missing field: {key}"
    print("Test 11 passed: All required fields present in transaction records")

    print("\nAll tests passed!")


# ============================================================
# CONCEPT: Private Data & Defensive Copying
# ------------------------------------------------------------
# DigitalWallet uses private attributes (__balance,
# __transaction_history, __transaction_counter) to prevent
# external code from tampering with internal state.
#
# Key encapsulation techniques:
#   1. Private double-underscore attributes enforce name
#      mangling so internals stay hidden.
#   2. A read-only @property (balance) exposes state
#      without granting write access.
#   3. get_transaction_history() uses deepcopy() so
#      callers receive a snapshot — mutating the returned
#      list does NOT affect the wallet's internal records.
#   4. An internal helper __add_transaction() centralises
#      record-keeping logic and auto-increments txn IDs.
# ============================================================

if __name__ == "__main__":
    main()
