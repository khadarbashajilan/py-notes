
class HealerMixin:
    """Provides healing capabilities to any character class."""
    def heal(self, target, amount):
        if not self.is_alive:
            print(f"❌ {self.name} cannot heal while defeated!")
            return
        target.health += amount
        print(f"✨ {self.name} heals {target.name} for {amount} HP!")
