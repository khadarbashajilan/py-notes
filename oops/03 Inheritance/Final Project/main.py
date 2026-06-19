from characters import Mage, Archer, Warrior, Paladin
from engine import battle

def main():
    # Initialize your characters
    gandalf = Mage("Gandalf", health=80, attack_power=25, mana=20)
    legolas = Archer("Legolas", health=90, attack_power=20, arrows=3)
    arthas = Paladin("Arthas", health=120, attack_power=15)

    # Let's run a match!
    battle(gandalf, legolas)

if __name__ == "__main__":
    main()
