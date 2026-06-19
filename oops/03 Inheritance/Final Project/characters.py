from mixins import HealerMixin

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other):
        other.health -= self.attack_power
        print(f"⚔️ {self.name} attacks {other.name} for {self.attack_power} damage!")

    @property
    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name} (HP: {self.health})"


class Warrior(Character):
    def shield_block(self):
        print(f"🛡️ {self.name} raises their shield to block!")

    def attack(self, other):
        # Warriors don't use limited resources, so they never struggle!
        damage = self.attack_power * 1.5
        other.health -= damage
        print(f"💥 {self.name} delivers a Heavy Strike on {other.name} for {damage} damage!")


class Mage(Character):
    def __init__(self, name, health, attack_power, mana):
        super().__init__(name, health, attack_power)
        self.mana = mana

    def attack(self, other):
        if self.mana >= 10:
            self.mana -= 10
            other.health -= self.attack_power
            print(f"🔮 {self.name} casts a spell on {other.name} for {self.attack_power} damage! (Mana left: {self.mana})")
        else:
            # Option B: Fallback struggle attack
            damage = 2
            other.health -= damage
            print(f"👊 {self.name} is out of mana and desperately punches {other.name} for {damage} damage!")


class Archer(Character):
    def __init__(self, name, health, attack_power, arrows):
        super().__init__(name, health, attack_power)
        self.arrows = arrows

    def attack(self, other):
        if self.arrows >= 1:
            self.arrows -= 1
            other.health -= self.attack_power
            print(f"🏹 {self.name} shoots an arrow at {other.name} for {self.attack_power} damage! (Arrows left: {self.arrows})")
        else:
            # Option B: Fallback struggle attack
            damage = 2
            other.health -= damage
            print(f"🪓 {self.name} is out of arrows and swings their bow as a club for {damage} damage!")


class Paladin(Character, HealerMixin):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)
