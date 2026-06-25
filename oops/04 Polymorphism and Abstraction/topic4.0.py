import time

# A context manager for tracing the how much time it take to compile the code or return the output

#1
class Timer():

    def __enter__(self):
        """Start the timer when entering the 'with' block."""
        self.start_time = time.time()
        return self

    def __exit__(self,exc_val,exc_type,exc_tb):
        """Stop the timer and print elapsed time when exiting the 'with' block."""
        elapsed = time.time() - self.start_time
        print(f"Elapsed : {elapsed:.2f}s")


with Timer():
    total = sum(range(10))
    print(total)

# 2
from contextlib import contextmanager

@contextmanager
def timer_with_contextmanager():
    """A simpler context manager using the @contextmanager decorator."""
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"Elapsed : {elapsed:.2f}s")


with timer_with_contextmanager():
    total = sum(range(10))
    print((total))


# ==========================================
# CONCEPT: CONTEXT MANAGERS
# ==========================================
#
# A Context Manager controls what happens BEFORE and AFTER a block
# of code using the "with" statement. Think of it as:
#   "Set something up -> do work -> clean up"
#
# TWO WAYS TO CREATE THEM:
#
# 1) CLASS-BASED (Timer class):
#    - __enter__(): runs when you enter the "with" block
#    - __exit__(): runs when you leave the "with" block (even if error!)
#    - More explicit, good for complex setup/teardown
#
# 2) DECORATOR-BASED (@contextmanager):
#    - Use "yield" to split setup from teardown
#    - Code before yield = setup, code after yield = cleanup
#    - More concise, good for simple cases
#
# WHY USE CONTEXT MANAGERS?
#   - Automatically clean up resources (files, connections, timers)
#   - Exception-safe: cleanup happens even if an error occurs
#   - Cleaner code than try/finally blocks
#
# COMMON USES:
#   - with open("file.txt") as f:  # auto-closes file
#   - with database.connect() as db:  # auto-closes connection
#   - with Timer():  # auto-measures time
