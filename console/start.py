__author__ = 'uzumaxy'

from core.computer import Computer
from time import sleep
from os import linesep

# Initialize computer instance
computer = Computer()

# Begin printing information
print('Start monitoring system.')
print('-' * 64)

# Display general information about computer
print('Hostname: ' + str(computer.hostname))
print('OS: ' + str(computer.os))
print('Boot time: ' + str(computer.boot_time))

# Display memory info for next ~8 seconds
computer.nonvolatile_memory.start_monitoring()
computer.virtual_memory.start_monitoring()
for _ in range(8):
    print('Nonvolatile memory: used {0} from {1}, {2} {3}'.format(
        computer.nonvolatile_memory.total,
        computer.nonvolatile_memory.available,
        computer.nonvolatile_memory.percent,
        linesep
    ))
    print('Virtual memory: used {0} from {1}, {2} {3}'.format(
        computer.virtual_memory.total,
        computer.virtual_memory.available,
        computer.virtual_memory.percent,
        linesep
    ))
    sleep(1)

# Shutdown
computer.nonvolatile_memory.stop_monitoring()
computer.virtual_memory.stop_monitoring()
sleep(1)
print('-' * 64)
print('Shutdown monitoring system.')