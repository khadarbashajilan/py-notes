import os
import tempfile
from contextlib import contextmanager

# A context manager that creates a temporary file and guarantees its deletion — even if an error occurs.

class TempFileManager:
    def __init__(self, content="", suffix=".txt"):
        """Set the content and file extension for the temp file."""
        self.content = content
        self.suffix = suffix
        self.filepath = None

    def __enter__(self):
        """Create a temporary file and return its path."""
        with tempfile.NamedTemporaryFile(
                mode='w', suffix=self.suffix, delete=False
                ) as tmp:
            if self.content:
                tmp.write(self.content)

            self.filepath = tmp.name

        print(f"Created: {self.filepath}")
        return self.filepath

    def __exit__(self, ecx_type, exc_val, exc_tb):
        """Delete the temporary file when exiting the 'with' block."""
        if self.filepath and os.path.exists(self.filepath):
            os.unlink(self.filepath)
            print(f"Deleted : {self.filepath}")

        return False

with TempFileManager("Imp data .... ") as filepath:
    with open(filepath) as f:
        print(f.read())
    print(f"File exists: {os.path.exists(filepath)}")
print(f"File exists after : {os.path.exists(filepath)}")

print()

# Test with exception:
try:
    with TempFileManager("Important data") as filepath:
        raise RuntimeError("Oops!")
except RuntimeError:
    print(f"File cleaned up? {not os.path.exists(filepath)}")



print()

@contextmanager
def TempFileManager_with_contextmanager(content="", suffix=".txt"):
    """Same TempFileManager but using the @contextmanager decorator."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix=suffix, delete=False
            ) as tmp:
        if content:
            tmp.write(content)
        filepath = tmp.name
    print(f"Created : {filepath}")

    try:
        yield filepath
    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)
            print(f"Deleted : {filepath}")

with TempFileManager_with_contextmanager("Some text ....") as f:
    with open(f) as f_:
        print(f_.read())
    print(f"File exists : {os.path.exists(f)}")
print(f"File exists : {os.path.exists(f)}")


# ==========================================
# CONCEPT: CONTEXT MANAGERS WITH RESOURCE CLEANUP
# ==========================================
#
# This file shows a PRACTICAL use of context managers: creating
# temporary files that are GUARANTEED to be deleted afterwards.
#
# WHY IS THIS USEFUL?
#   - Temp files often hold sensitive data or large results
#   - If you forget to delete them, your disk fills up
#   - If an error occurs mid-process, normal cleanup code is skipped
#   - Context managers solve both problems automatically
#
# HOW IT WORKS:
#   __enter__: Creates a temp file using tempfile.NamedTemporaryFile
#              with delete=False (so it persists for reading)
#   __exit__:  Checks if file exists, deletes it if so
#              Works even if an exception occurred inside the "with" block
#
# GUARANTEED CLEANUP:
#   The __exit__ method is ALWAYS called, even if:
#     - An exception is raised
#     - You use "return" inside the with block
#     - The program crashes (in most cases)
#
# CLASS-BASED vs DECORATOR-BASED:
#   Both versions do the same thing. The @contextmanager version
#   is shorter but the class-based version is easier to understand
#   for beginners.
#
# RETURN False in __exit__:
#   This tells Python "don't suppress the exception" — let it propagate.
#   If we returned True, the exception would be silently swallowed.
