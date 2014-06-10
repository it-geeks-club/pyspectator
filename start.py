from console import start as start_console
from pyspectator.computer import Computer

# Initialize computer instance
computer = Computer()
with computer:
    # Start console interface
    start_console(computer)