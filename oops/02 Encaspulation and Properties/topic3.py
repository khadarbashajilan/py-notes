import re

class User:

    def __init__(self, username):
        self.username = username

    @property
    def username(self):
        return self._username

    def is_valid(self, s):
        if not isinstance(s, str):
            raise TypeError(f"Username must be a string, instead we got {type(s).__name__}")

        s = s.strip()

        if not s:
            raise ValueError("Username cannot be empty or whitespace")

        if " " in s:
            raise ValueError("Username cannot contain spaces")

        if len(s) < 3 or len(s) > 20:
            raise ValueError(f"Username must be between 3 and 20 characters, got {len(s)}")

        for ch in s:
            if not (ch.isalnum() or ch == "_"):
                raise ValueError(
                    f"Username can only contain letters, numbers, and underscores. "
                    f"Invalid character: '{ch}'"
                )

    @username.setter
    def username(self, value):
        #self.is_valid(value)
        
        if not isinstance(value, str):
            raise TypeError(f"Username must be a string, instead we got {type(value).__name__}")
            

        if not re.match(r"^\w{3,20}$", value.strip()):
            raise ValueError(
                    "Username must be between 3 and 20 characters and "
            "can only contain letters, numbers, and underscores (no spaces)."
        )

        self._username = value.strip()


# ============================================
# QUICK TEST CASES
# ============================================

# Valid cases
print("✓ Valid usernames:")
u1 = User("john")
print(f"  {u1.username}")

u2 = User("python_dev")
print(f"  {u2.username}")

u3 = User("  alice  ")  # strips whitespace
print(f"  {u3.username}")

# TypeError cases
print("\n✓ TypeError:")
try:
    User(123)
except TypeError as e:
    print(f"  {e}")

try:
    User(None)
except TypeError as e:
    print(f"  {e}")

# ValueError cases
print("\n✓ ValueError:")
try:
    User("ab")  # too short
except ValueError as e:
    print(f"  {e}")

try:
    User("user name")  # has space
except ValueError as e:
    print(f"  {e}")

try:
    User("user@name")  # invalid char
except ValueError as e:
    print(f"  {e}")

# Setter validation
print("\n✓ Setter validation:")
u4 = User("initial")
try:
    u4.username = "bad name"  # space in name
except ValueError as e:
    print(f"  {e}")

print(f"  Still unchanged: {u4.username}")

u4.username = "changed"
print(f"  Updated: {u4.username}")

print("\n✅ All tests passed!")

#----------------------------------------------------------------------------------

class Email:
    def __init__(self, email):
        self.email = email
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        # Step 1: Type check
        if not isinstance(value, str):
            raise TypeError(
                f"Email must be a string, got {type(value).__name__}"
            )
        
        value = value.strip()
        
        # Step 2: Check exactly one @
        if value.count('@') != 1:
            raise ValueError(
                f"Email must contain exactly one '@' symbol. Got: '{value}'"
            )
        
        username, domain = value.split('@')
        
        # Step 3: Username length
        if len(username) < 3 or len(username) > 15:
            raise ValueError(
                f"Username part must be 3-15 characters, "
                f"got {len(username)}: '{username}'"
            )
        
        # Step 4: Username characters
        for ch in username:
            if not (ch.isalnum() or ch in "._"):
                raise ValueError(
                    f"Username can only contain letters, numbers, dots, "
                    f"and underscores. Invalid character: '{ch}'"
                )
        
        # Step 5: Domain length
        if len(domain) < 3:
            raise ValueError(
                f"Domain must be at least 3 characters. Got: '{domain}'"
            )
        
        # Step 6: Domain dot structure
        if '.' not in domain:
            raise ValueError(
                f"Domain must contain a dot. Got: '{domain}'"
            )
        
        if domain.startswith('.') or domain.endswith('.'):
            raise ValueError(
                f"Domain dot cannot be at start or end. Got: '{domain}'"
            )
        
        # Step 7: No spaces in domain
        if ' ' in domain:
            raise ValueError(
                f"Domain cannot contain spaces. Got: '{domain}'"
            )
        
        self._email = value       
        

# Tests
print("✓ Valid:")
e1 = Email("john@gmail.com")
print(f"  {e1.email}")

e2 = Email("alice_123@web.co")
print(f"  {e2.email}")

try:
    Email(123)
except TypeError as e:
    print(f"✓ TypeError: {e}")

try:
    Email("noatsign")
except ValueError as e:
    print(f"✓ ValueError: {e}")

try:
    Email("a@b.c")  # username too short
except ValueError as e:
    print(f"✓ ValueError: {e}")

try:
    Email("user@@mail.com")
except ValueError as e:
    print(f"✓ ValueError: {e}")

# Test setter
e3 = Email("test@mail.com")
try:
    e3.email = "bad email@mail.com"
except ValueError as e:
    print(f"✓ Setter validation: {e}")
print(f"  Still: {e3.email}")

print("\n✅ Done!")
