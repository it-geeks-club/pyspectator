from time import sleep
from console import start as start_console
from pyspectator.computer import Computer

try:
    # Initialize computer instance
    computer = Computer()
    computer.start_monitoring()
    computer.processor.start_monitoring()
    for mem in computer.nonvolatile_memory:
        mem.start_monitoring()
    computer.virtual_memory.start_monitoring()

    # Start console interface
    start_console(computer)
except:
    pass
finally:
    # Shutdown
    computer.processor.stop_monitoring()
    for mem in computer.nonvolatile_memory:
        mem.stop_monitoring()
    computer.virtual_memory.stop_monitoring()
    computer.stop_monitoring()
    sleep(1)