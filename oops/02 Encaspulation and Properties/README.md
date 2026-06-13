# Encapsulation & Properties — Theory & Revision Notes

Python OOP encapsulation — access modifiers, property decorators, validation, and data protection. These notes explain the *theory* first; use them as a primer before attempting interview questions.

---

## Topic 1 — `topic1.py` (Access Modifiers: Public, Protected, Private)

### Core Concepts

**Public attributes:**
- No underscore prefix. Freely readable and writable from outside the class.
- Part of the "official" public interface. Documented and expected to be used by consumers.

**Protected attributes (`_var`):**
- Single underscore prefix. A **convention only** — Python does not enforce it.
- Signals to other developers: "This is for internal use. Don't access or modify it directly."
- Still fully accessible from outside (`obj._var` works). Relies on developer discipline.
- Used when a subclass needs access but external code should be discouraged.

**Private attributes (`__var`):**
- Double underscore prefix. Triggers **name mangling** — Python renames `__var` to `_ClassName__var`.
- Prevents accidental access and avoids name clashes in subclasses.
- Not truly private (still accessible via the mangled name `obj._ClassName__var`), but accessing it that way is a code smell.
- Accessing `obj.__var` directly raises `AttributeError`.

### Name Mangling Mechanics

```python
class Hero:
    def __init__(self):
        self.__password = "secret"   # Stored as _Hero__password

h = Hero()
h.__password          # AttributeError (name-mangled)
h._Hero__password     # 'secret' (accessible but discouraged)
```

- Mangling happens at class definition time. The `__` prefix causes Python to rewrite the name.
- This prevents subclass accidental overrides — a child class defining `__password` gets `_Child__password`, separate from `_Parent__password`.

### Key Design Points

| Concept | Syntax | Accessibility | Enforcement |
|---------|--------|---------------|-------------|
| Public | `self.var` | Unlimited | None |
| Protected | `self._var` | Discouraged externally | Convention only |
| Private | `self.__var` | Name-mangled | Python-internal (still hackable) |

### Common Pitfalls
- **Protected is not enforced:** `obj._var` works just fine. The underscore is a gentleman's agreement.
- **Private is not truly private:** The mangled name `_ClassName__var` is predictable and accessible.
- **Outside vs inside:** Inside the class, `self.__var` works normally. Outside, it's `self._ClassName__var`.
- **Name mangling and inheritance:** Each class gets its own mangled namespace — child class `__var` doesn't collide with parent `__var`.

---

## Topic 2 — `topic2.py` (Properties: Read-Only, Validated Setters, Computed Properties)

### Core Concepts

**The `@property` decorator:**
- Transforms a method into a **read-only attribute** access.
- Allows you to define logic that runs when an attribute is *read*, while keeping the interface clean.
- The method name becomes the property name — used without parentheses.

**The `@<property>.setter` decorator:**
- Defines logic that runs when the attribute is *assigned*.
- Enables **validation**, transformation, or side effects on assignment.
- The setter method must have the same name as the property.

**Read-only properties:**
- A property with no setter. Cannot be assigned from outside.
- Ideal for fixed identity fields (account number, student ID, etc.).

**Computed properties:**
- A property whose value is calculated from other attributes on every access.
- No backing data needed — the computation happens in the getter.
- Examples: `area`, `perimeter`, `is_overdrawn`, `letter_grade`.

### Property Flow

```
obj.balance      →  @balance.getter  → returns self._balance
obj.balance = x  →  @balance.setter  → validates, then self._balance = x
```

### Pattern: Property + Backing Attribute

```python
@property
def balance(self):
    return self._balance            # Backing attribute

@balance.setter
def balance(self, amount):
    if amount < 0:
        raise ValueError(...)       # Validation
    self._balance = amount          # Backing attribute
```

The backing attribute (`_balance`) is conventionally the property name prefixed with `_`. It is the "real" storage; the property is the gateway.

### Comparison

| Pattern | Getter | Setter | Use Case |
|---------|--------|--------|----------|
| Read-only | ✅ | ❌ | Identity fields (account_number, name) |
| Validated | ✅ | ✅ with validation | Data that must satisfy constraints (grade, balance) |
| Computed | ✅ computed on read | ❌ | Derived values (area, letter_grade, is_square) |

### Key Design Points

| Concept | Explanation |
|---------|-------------|
| `@property` | Makes a method look like an attribute. Called on read. |
| `@x.setter` | Called on assignment. Run validation/logic before storing. |
| Backing attr `_x` | Stores the actual value. Convention to prefix with `_`. |
| Read-only | Property with getter only. Assignment raises `AttributeError`. |
| Computed property | Value derived from other attrs. No backing storage needed. |

### Common Pitfalls
- **Set and getter naming:** The setter and getter methods must have the **same name** as each other and as the property.
- **Backing attribute name collision:** If you name the backing attribute the same as the property, you'll get infinite recursion (getter calls `self.x`, which calls the getter again).
- **Validation in `__init__`:** Setting `self.balance = ...` in `__init__` automatically goes through the setter — validation runs. Use this intentionally.
- **Computed properties aren't cached:** The computation runs on every access. For expensive computations, consider caching (`@functools.cached_property` for immutable data).

---

## Topic 3 — `topic3.py` (Property Validation with Type & Format Checking)

### Core Concepts

**Type validation in setters:**
- Use `isinstance(value, type)` to enforce the expected type.
- Raise `TypeError` with a descriptive message when the wrong type is passed.
- Catches bugs early — a username should always be a string, never an int or None.

**Format validation in setters:**
- Use regular expressions (`re.match`) to enforce structural constraints.
- Examples: username (alphanumeric, 3-20 chars), email (one `@`, valid domain).
- Raise `ValueError` with a descriptive message explaining the constraint.

### Validation Patterns

**The `@property` validator pattern:**
```python
@property
def username(self):
    return self._username

@username.setter
def username(self, value):
    if not isinstance(value, str):          # 1. Type check
        raise TypeError(...)
    if not re.match(r"^\w{3,20}$", value):  # 2. Format check
        raise ValueError(...)
    self._username = value.strip()          # 3. Clean & store
```

**Setter atomicity (fail-safe behavior):**
- If the setter raises an exception, the attribute remains **unchanged**.
- This is because the exception is raised *before* `self._attr = value` executes.
- Verified in tests: after a failed setter call, the original value is preserved.

### Multi-Step Validation (Email Example)

| Step | Check | Error Type |
|------|-------|------------|
| 1 | Is it a string? | `TypeError` |
| 2 | Exactly one `@`? | `ValueError` |
| 3 | Username 3-15 chars? | `ValueError` |
| 4 | Username valid chars? | `ValueError` |
| 5 | Domain ≥ 3 chars? | `ValueError` |
| 6 | Domain contains `.`? | `ValueError` |
| 7 | Domain doesn't start/end with `.`? | `ValueError` |
| 8 | Domain no spaces? | `ValueError` |

Each check fails fast with a specific, actionable error message.

### Key Design Points

| Concept | Explanation |
|---------|-------------|
| `isinstance` check | First gate — rejects wrong types before format checks |
| `re.match` | Anchored at string start — must match entire string |
| `value.strip()` | Normalize input before storing (and before validation where needed) |
| `TypeError` vs `ValueError` | `TypeError` for wrong type; `ValueError` for wrong value/format |
| Atomic setter | If setter raises, original value is preserved — no partial updates |

### Common Pitfalls
- **`re.match` vs `re.search`:** `re.match` only matches at the beginning of the string. Use it with `\w{3,20}$` to ensure the entire string matches.
- **`re.match` anchors:** Always use `^` and `$` in the pattern to enforce full-string matching, or use `re.fullmatch`.
- **Validation order:** Check type first (raises `TypeError`), then format (raises `ValueError`). This gives callers clearer error messages.
- **Whitespace:** If you strip input, strip it consistently before validation (or the length check may fail due to leading/trailing spaces).

---

## Topic 4 — `topic4.py` (Encapsulation: Private Data & Controlled Access)

### Core Concepts

**Encapsulation via private attributes:**
- Sensitive or internal state (balance, transaction history) is stored in `__` private attributes.
- External code cannot accidentally modify these — they must go through public methods.
- This protects invariants (e.g., balance can never go negative).

**Controlled access via public methods:**
- `deposit(amount)` — validates and adds money.
- `withdraw(amount)` — validates and subtracts money.
- Public methods enforce business rules before mutating state.

**Read-only access via `@property`:**
- `balance` is exposed as a read-only property — external code can check it but not modify it.
- No setter means the only way to change balance is through `deposit()` / `withdraw()`.

**Data integrity via `deepcopy`:**
- `get_transaction_history()` returns a `deepcopy` of the internal history list.
- Callers can mutate the returned copy without affecting internal state.
- This prevents external code from corrupting the transaction log.

### Wallet Transaction Flow

```
User calls deposit(50)
  → Validate amount (type check, amount > 0)
  → self.__balance += 50
  → __add_transaction('Deposit', 50)
      → Increment __transaction_counter
      → Append {
          'id': 1,
          'type': 'Deposit',
          'amount': 50,
          'balance': 150,
          'timestamp': datetime.now()
        }
  → Return "Successful Deposit"
```

### The `__add_transaction` Pattern

- A **private helper method** (double underscore) — only used internally.
- Encapsulates the logic of building a transaction record.
- Automatically called after every successful `deposit` or `withdraw`.
- The method itself accesses private attributes (`__balance`, `__transaction_counter`).

### Key Design Points

| Concept | Explanation |
|---------|-------------|
| Private `__balance` | No direct assignment from outside — only via `deposit`/`withdraw` |
| Read-only `@property` balance | External read allowed, write prohibited — no setter |
| Private `__transaction_history` | Internal log — external reads go through `deepcopy` |
| `__add_transaction` | Private helper — enforces consistent record format |
| `deepcopy` | Returns independent copy — caller mutations don't affect internal state |

### Common Pitfalls
- **Returning mutable internals:** Returning `self.__transaction_history` directly lets callers modify internal state. Always return a copy.
- **`deepcopy` vs `copy`:** `deepcopy` copies nested structures (dicts within lists). `shallow copy` (`list.copy()`) would share the inner dicts.
- **`__init__` bypassing setters:** If the class had setters, calling `self.balance = X` in `__init__` would trigger validation. Here, directly setting `self.__balance = 0` in init bypasses any setter — deliberate for this design.
- **Performance of `deepcopy`:** For transaction logs with many entries, consider pagination or limiting the returned copy size.

---

## Quick Reference: Encapsulation & Properties in Python

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Public attribute | `self.x = val` | Free access |
| Protected attribute | `self._x = val` | Internal use (convention) |
| Private attribute | `self.__x = val` | Name-mangled (harder to access) |
| Read-only property | `@property def x(self):` | Attribute reads with logic |
| Validated setter | `@x.setter def x(self, val):` | Attribute writes with validation |
| Computed property | `@property` (no storage) | Derived value on read |
| Type validation | `isinstance(val, type)` | Reject wrong types |
| Format validation | `re.match(pattern, val)` | Reject malformed strings |
| Deep copy for safety | `deepcopy(internal_list)` | Prevent caller mutation |

---

## Common Gotchas

1. **Name mangling:** `self.__x` becomes `_ClassName__x` — accessible but not recommended.
2. **Protected is convention:** `self._x` is fully accessible — no enforcement.
3. **Property recursion:** Naming the backing attr the same as the property causes infinite recursion.
4. **Setter atomicity:** If the setter raises, the attribute value is preserved — no partial updates.
5. **TypeError vs ValueError:** Wrong type → `TypeError`; Wrong value → `ValueError`.
6. **`re.match` anchoring:** Without `$`, `re.match(r"\w{3,20}", "verylongstring")` still matches — it only checks the start.
7. **Mutable returns:** Always return `deepcopy` of internal mutable objects to prevent caller corruption.
8. **Validation in `__init__`:** If you set via `self.prop = val` in init, the setter runs — and its validation runs too.
9. **Computed properties aren't cached:** Each access re-runs the computation.
10. **No setter → immutable:** A property without a setter silently raises `AttributeError` on assignment.
