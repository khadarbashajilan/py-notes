import re


class User:
    """Demonstrates a validated username property with type/format checking."""

    def __init__(self, username):
        """Initialize user with a validated username."""
        self.username = username  # Uses setter — validation runs automatically

    @property
    def username(self):
        """Return the validated username."""
        return self._username

    @username.setter
    def username(self, value):
        """Validate and set username: 3-20 alphanumeric chars or underscores, no spaces."""
        if not isinstance(value, str):
            raise TypeError(
                f"Username must be a string, instead we got {type(value).__name__}"
            )

        if not re.match(r"^\w{3,20}$", value.strip()):
            raise ValueError(
                "Username must be between 3 and 20 characters and "
                "can only contain letters, numbers, and underscores (no spaces)."
            )

        self._username = value.strip()


class Email:
    """Demonstrates a validated email property with multi-step format checking."""

    def __init__(self, email):
        """Initialize with a validated email address."""
        self.email = email  # Uses setter — validation runs automatically

    @property
    def email(self):
        """Return the validated email."""
        return self._email

    @email.setter
    def email(self, value):
        """Validate and set email: exactly one @, 3-15 char username, valid domain."""
        if not isinstance(value, str):
            raise TypeError(
                f"Email must be a string, got {type(value).__name__}"
            )

        value = value.strip()

        if value.count('@') != 1:
            raise ValueError(
                f"Email must contain exactly one '@' symbol. Got: '{value}'"
            )

        username, domain = value.split('@')

        if len(username) < 3 or len(username) > 15:
            raise ValueError(
                f"Username part must be 3-15 characters, "
                f"got {len(username)}: '{username}'"
            )

        for ch in username:
            if not (ch.isalnum() or ch in "._"):
                raise ValueError(
                    f"Username can only contain letters, numbers, dots, "
                    f"and underscores. Invalid character: '{ch}'"
                )

        if len(domain) < 3:
            raise ValueError(
                f"Domain must be at least 3 characters. Got: '{domain}'"
            )

        if '.' not in domain:
            raise ValueError(
                f"Domain must contain a dot. Got: '{domain}'"
            )

        if domain.startswith('.') or domain.endswith('.'):
            raise ValueError(
                f"Domain dot cannot be at start or end. Got: '{domain}'"
            )

        if ' ' in domain:
            raise ValueError(
                f"Domain cannot contain spaces. Got: '{domain}'"
            )

        self._email = value


def main():
    """Test User and Email validation logic with valid and invalid inputs."""

    # ---------- User Tests ----------
    print("=== User ===")

    # Valid usernames
    u1 = User("john")
    assert u1.username == "john"
    print("Test 1: Valid username 'john'")

    u2 = User("python_dev")
    assert u2.username == "python_dev"
    print("Test 2: Valid username 'python_dev'")

    u3 = User("  alice  ")
    assert u3.username == "alice"
    print("Test 3: Whitespace stripped from username")

    # TypeError cases
    try:
        User(123)
        assert False
    except TypeError:
        print("Test 4: Non-string username (int) rejected")

    try:
        User(None)
        assert False
    except TypeError:
        print("Test 5: Non-string username (None) rejected")

    # ValueError cases
    try:
        User("ab")
        assert False
    except ValueError:
        print("Test 6: Too-short username rejected")

    try:
        User("user name")
        assert False
    except ValueError:
        print("Test 7: Username with space rejected")

    try:
        User("user@name")
        assert False
    except ValueError:
        print("Test 8: Username with invalid char rejected")

    # Setter validation
    u4 = User("initial")
    try:
        u4.username = "bad name"
        assert False
    except ValueError:
        print("Test 9: Setter rejects username with space")

    assert u4.username == "initial", "Original value preserved on setter failure"
    print("Test 10: Original value unchanged after failed setter")

    u4.username = "changed"
    assert u4.username == "changed"
    print("Test 11: Setter accepts valid update")

    # ---------- Email Tests ----------
    print("\n=== Email ===")

    e1 = Email("john@gmail.com")
    assert e1.email == "john@gmail.com"
    print("Test 12: Valid email 'john@gmail.com'")

    e2 = Email("alice_123@web.co")
    assert e2.email == "alice_123@web.co"
    print("Test 13: Valid email 'alice_123@web.co'")

    try:
        Email(123)
        assert False
    except TypeError:
        print("Test 14: Non-string email (int) rejected")

    try:
        Email("noatsign")
        assert False
    except ValueError:
        print("Test 15: Email without @ rejected")

    try:
        Email("a@b.c")
        assert False
    except ValueError:
        print("Test 16: Too-short username rejected")

    try:
        Email("user@@mail.com")
        assert False
    except ValueError:
        print("Test 17: Double @ rejected")

    # Setter validation
    e3 = Email("test@mail.com")
    try:
        e3.email = "bad email@mail.com"
        assert False
    except ValueError:
        print("Test 18: Setter rejects email with space in domain")

    assert e3.email == "test@mail.com", "Original value preserved on setter failure"
    print("Test 19: Original value unchanged after failed setter")

    print("\nAll tests passed!")


# ============================================================
# CONCEPT: Validation via Property Setters
# ------------------------------------------------------------
# Property setters allow us to intercept attribute assignment
# and enforce rules — type checks, length limits, format
# matching via regex (e.g., \w{3,20}), and domain structure.
#
# User   — validates username: string, 3-20 alphanumeric/_
# Email  — validates email: exactly one @, 3-15 char local
#          part, valid domain with dot, no spaces.
#
# On failure, the setter raises TypeError or ValueError
# and the internal state remains unchanged (the old value
# is preserved — demonstrated in tests).
# ============================================================

if __name__ == "__main__":
    main()
