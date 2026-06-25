# Inheritance Battle Arena — OOP-Driven Turn-Based Combat

A turn-based battle simulator built to demonstrate Python OOP principles including **inheritance**, **polymorphism**, **mixins**, and **encapsulation**. Characters with unique abilities fight until one falls.

## How OOP Solves the Problem

Without OOP, we'd write a sprawling script of conditional checks — `if character_type == "mage"` scattered everywhere, duplicate health/attack logic for each class, and no clean way to add new character types. Every new feature would risk breaking existing code.

OOP organizes combat around a shared `Character` base class. Common attributes (`name`, `health`, `attack_power`) and behaviors (`attack`, `is_alive`) live in one place. Each subclass — `Warrior`, `Mage`, `Archer`, `Paladin` — **inherits** the base and **overrides** only what makes it unique. The `battle` function treats every character identically through **polymorphism**, calling the same `attack()` method while each subclass delivers different behavior. A `HealerMixin` adds cross-cutting healing without polluting the class hierarchy.

## Method-by-Method Breakdown

### `Character.__init__` — *constructor*

Stores a character's `name`, `health`, and `attack_power`. These attributes are the shared data contract that every subclass builds upon.

### `Character.attack` — *method*

Subtracts `attack_power` from the opponent's health. This is the **default implementation** — subclasses override it to deliver class-specific combat logic (mana consumption, arrow tracking, damage multipliers).

### `Character.is_alive` — *property*

Returns `True` if `health > 0`. Encapsulates the "alive" check so the battle engine and mixins never inspect `health` directly.

### `Character.__str__` — *dunder method*

Returns a readable string like `"Gandalf (HP: 80)"`. Used by the battle engine to display character status each round.

### `Warrior.attack` — *override*

Multiplies `attack_power` by 1.5 for a Heavy Strike. Warriors have no resource constraints — demonstrating a subclass that **strengthens** behavior without adding state.

### `Mage.attack` — *override*

Checks `mana >= 10` before casting. If mana is low, falls back to a weak 2-damage punch. Shows **conditional resource management** through method overriding.

### `Mage.__init__` — *constructor override*

Calls `super().__init__` to reuse the parent constructor, then adds a `mana` attribute. Demonstrates **constructor chaining**.

### `Archer.attack` — *override*

Spends an arrow on each shot. When arrows run out, the archer swings their bow as a club for 2 damage. Mirrors the Mage's resource-fallback pattern.

### `Paladin` — *multiple inheritance*

Inherits from both `Character` and `HealerMixin`. Has no override of its own — it receives the base `attack` and the mixin's `heal` method simultaneously.

### `HealerMixin.heal` — *mixin method*

Adds health to a target character. Guards against healing while defeated by checking `self.is_alive`. The mixin assumes the host class provides `name` and `is_alive` — a **contract via duck typing**.

### `battle(c1, c2)` — *module-level function*

Runs a round-robin loop alternating attacks between two characters. Checks `is_alive` before each turn and prints the victor. This function works with **any** `Character` subclass — no type checks needed.

### `main` — *entry point*

Instantiates a `Mage`, `Archer`, and `Paladin`, then calls `battle(...)`. A minimal example that proves the class hierarchy works end-to-end.

## OOP Pillars Demonstrated

| Pillar | How It's Used |
|---|---|
| **Encapsulation** | `is_alive` property hides the health check; `__init__` bundles state with behavior |
| **Inheritance** | `Warrior`, `Mage`, `Archer`, `Paladin` extend `Character`, reusing fields and default methods |
| **Polymorphism** | `battle()` calls `c1.attack(c2)` and each subclass runs its own version — no `isinstance` needed |
| **Abstraction** | `HealerMixin` requires only `name` and `is_alive` without knowing the full class; `battle()` works against any `Character` |

## Files

| File | Purpose |
|---|---|
| `characters.py` | Base `Character` class and four subclass definitions (`Warrior`, `Mage`, `Archer`, `Paladin`) |
| `engine.py` | `battle()` function that orchestrates turn-based combat between two characters |
| `mixins.py` | `HealerMixin` providing a reusable `heal()` method via multiple inheritance |
| `main.py` | Application entry point that creates characters and starts a battle |
