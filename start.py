from time import sleep
from console import start as start_console
from pyspectator.computer import Computer

# Initialize computer instance
computer = Computer()
try:
    # Start monitoring
    computer.start_monitoring()
    computer.processor.start_monitoring()
    for mem in computer.nonvolatile_memory:
        mem.start_monitoring()
    computer.virtual_memory.start_monitoring()
    computer.network_interface.start_monitoring()

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
    computer.network_interface.stop_monitoring()
    computer.stop_monitoring()
    sleep(1)