# Encapsulation and Properties — Bank Account System

A simple bank account system demonstrating **encapsulation** and **properties** in Python.

## How OOP Solves the Problem

Without OOP, we'd track a balance and transaction log as separate global variables with loose functions modifying them directly. Nothing prevents accidental overwrites or invalid states.

OOP lets us **encapsulate** the balance and transaction history as private attributes inside an `Account` class. The only way to interact with them is through controlled methods (`deposit`, `withdraw`) and read-only properties (`balance`, `transaction_count`). This guarantees the account balance can never be set to an invalid value, and all changes are audited via the transaction log.

## The `Account` Class — Method by Method

### `__init__(self)`
Constructor. Initializes a new account with a balance of `0` and an empty transaction list. Both are stored as **private attributes** (`__balance`, `__transactions`) to prevent direct tampering from outside the class.

### `balance` — *property*
Read-only property. Returns the current balance. Since `__balance` is private, this property is the **only** way external code can check the balance. There is no setter — meaning you cannot accidentally overwrite it.

### `transaction_count` — *property*
Read-only property. Returns how many transactions (deposits + withdrawals) have been performed. Drives home the same encapsulation principle: internal state is exposed only through intentional interfaces.

### `deposit(self, amount)`
Instance method. Accepts an integer or float. Validates that the amount is a number and greater than zero, then adds it to `__balance`. Logs the transaction with type, amount, and resulting balance. **Validation before mutation** ensures the balance can never become inconsistent.

### `withdraw(self, amount)`
Instance method. Accepts an integer or float. Validates type, positive value, and **sufficient balance** before subtracting from `__balance`. If the amount exceeds available funds, a `ValueError` is raised — the balance is never overdrawn. Logs the transaction just like `deposit`.

### `get_statement(self)`
Instance method. Iterates over the private `__transactions` list and prints every transaction in a human-readable format (type, amount, balance after). This is the **only window** into the transaction history — the list itself cannot be modified from outside.

## OOP Pillars Demonstrated

| Pillar | How It's Used |
|---|---|
| **Encapsulation** | `__balance` and `__transactions` are private; all access goes through public methods and properties |
| **Properties** | `@property` decorators expose `balance` and `transaction_count` as read-only attributes with no setters |
| **Input Validation** | Every mutator method validates before mutating — preventing invalid state |
| **Self-Managing Objects** | Each `Account` instance owns its data and enforces its own invariants |

## Files

| File | Purpose |
|---|---|
| `main.py` | The `Account` class with all methods and properties |
