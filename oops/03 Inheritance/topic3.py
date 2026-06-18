class WalkingMovement:
    def move(self):
        """Return a string indicating walking movement."""
        return "is walking"

class TalkingSpeech:
    def speech(self):
        """Return a string with a greeting."""
        return "Hello World"

class DancingMovement:
    def move(self):
        """Return a string indicating dancing movement."""
        return "is doing the robot dance"

class SingingSpeech:
    def speech(self):
        """Return a string with a song lyric."""
        return "\U0001f3b5 Daisy, Daisy, give me your answer do... \U0001f3b5"

class Robot:
    def __init__(self,name, movement, speech):
        """Initialize a robot with a name, movement behavior, and speech behavior."""
        self.name = name
        self.movement = movement
        self.speech = speech

    def perform(self):
        """Execute the robot's movement and speech, returning a formatted string."""
        return f"{self.name} is {self.movement.move()} and also says {self.speech.speech()}"


robot = Robot("Robbie", WalkingMovement(), TalkingSpeech())
print(robot.perform())
dancing_robot = Robot("Bender", DancingMovement(), SingingSpeech())
print(dancing_robot.perform())


"""
================================================================================
CONCEPT: COMPOSITION (HAS-A Relationship)
================================================================================

1. Composition over Inheritance:
   - Instead of using inheritance ("is-a" relationship), the `Robot` class 
     uses composition ("has-a" relationship) by holding references to 
     movement and speech objects.
   - `Robot` *has a* movement behavior and *has a* speech behavior.

2. Delegation:
   - `Robot.perform()` delegates the actual behavior to its composed objects
     by calling `self.movement.move()` and `self.speech.speech()`.

3. Flexibility / Strategy Pattern:
   - Behaviors can be swapped at runtime without changing the `Robot` class.
   - `Robot("Robbie", WalkingMovement(), TalkingSpeech())` vs 
     `Robot("Bender", DancingMovement(), SingingSpeech())` — same Robot 
     class, completely different behaviors.

4. Loose Coupling:
   - `Robot` does not need to know how movement or speech works internally.
     It only relies on the interface (`.move()` and `.speech()` methods).
   - New movement or speech types can be added without modifying `Robot`.

5. Difference from Inheritance:
   - Inheritance: `class Robot(WalkingMovement, TalkingSpeech)` — rigid, 
     compile-time, single chain.
   - Composition: Inject dependencies — flexible, runtime-swappable.
================================================================================
"""
