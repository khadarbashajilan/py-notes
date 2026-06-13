class Hero:
    """Demonstrates public, protected, and private attribute access levels in Python."""

    def __init__(self, name, password):
        """Initialize hero with a public name, protected level, and private password."""
        # 1. PUBLIC ATTRIBUTE
        # Anyone can see or change this. It's part of the "official" interface.
        self.name = name

        # 2. PROTECTED ATTRIBUTE (Single Underscore _)
        # This signals to other developers: "This is for internal use.
        # Please use the level_up() method instead of changing this directly."
        self._level = 1

        # 3. PRIVATE ATTRIBUTE (Double Underscore __)
        # Python will "mangle" this name to _Hero__password to prevent
        # accidental access or name clashes in subclasses.
        self.__password = password

    def level_up(self):
        """Increase hero level by 1 — the proper way to modify _level."""
        self._level += 1

    def get_status(self):
        """Return a summary of the hero's public and protected state."""
        return f"Hero : {self.name}, Level: {self._level}"


def main():
    """Test public, protected, and private attribute access on Hero."""

    print("--- Creating our Hero ---")
    my_hero = Hero("Arthas", "frostmourne")

    # Test 1: Public attribute — freely readable and writable
    print(f"1. Public Name: {my_hero.name}")
    my_hero.name = "Lich King"
    print(f"   Updated Name: {my_hero.name}")

    # Test 2: Protected attribute — accessible but discouraged (convention only)
    print(f"\n2. Protected Level (Direct): {my_hero._level}")
    my_hero.level_up()
    print(f"   Level after level_up(): {my_hero.get_status()}")

    # Test 3: Private attribute — name-mangled, direct access raises AttributeError
    print("\n3. Trying to access private password directly...")
    try:
        print(my_hero.__password)
    except AttributeError as e:
        print(f"   ERROR: {e}")

    # Test 4: Private attribute accessed via mangled name (possible but not recommended)
    print(f"\n4. Accessing via Name Mangling: {my_hero._Hero__password}")

    print("\n--- Test Complete ---")


if __name__ == "__main__":
    main()
