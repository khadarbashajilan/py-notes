class Hero:
    def __init__(self, name, password):
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
        """The 'proper' way to increase the level."""
        self._level += 1

    def get_status(self):
        """Returns a summary of the hero's public/protected state."""
        return f"Hero : {self.name}, Level: {self._level}"

# ==========================================
# TEST CASES: Let's see these rules in action!
# ==========================================

if __name__ == "__main__":
    print("--- Creating our Hero ---")
    my_hero = Hero("Arthas", "frostmourne")

    # ✅ TEST 1: Public Access (The Front Yard)
    print(f"1. Public Name: {my_hero.name}")
    my_hero.name = "Lich King"
    print(f"   Updated Name: {my_hero.name}")

    # ⚠️ TEST 2: Protected Access (The Backyard Fence)
    # It works, but we are bypassing the intended logic.
    print(f"\n2. Protected Level (Direct): {my_hero._level}")
    
    # The "Correct" way to change it:
    my_hero.level_up()
    print(f"   Level after level_up(): {my_hero.get_status()}")

    # ❌ TEST 3: Private Access (The Hidden Safe)
    print("\n3. Trying to access private password directly...")
    try:
        # This will fail because Python renamed the variable!
        print(my_hero.__password) 
    except AttributeError as e:
        print(f"   ERROR: {e}")

    # 🔑 TEST 4: The "Mangled" Name (The Secret Key)
    # If you really need to see it, you have to use the mangled name.
    print(f"\n4. Accessing via Name Mangling: {my_hero._Hero__password}")
    
    print("\n--- Test Complete ---")
