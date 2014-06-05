from core.computer import Computer
from time import sleep
from console import start as start_console

# Initialize computer instance
computer = Computer()
computer.start_monitoring()
computer.processor.start_monitoring()
for mem in computer.nonvolatile_memory:
    mem.start_monitoring()
computer.virtual_memory.start_monitoring()

# Start console interface
start_console(computer)

# Shutdown
computer.processor.stop_monitoring()
for mem in computer.nonvolatile_memory:
    mem.stop_monitoring()
computer.virtual_memory.stop_monitoring()
sleep(1)