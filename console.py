import subprocess
import platform
from os import linesep
from time import sleep

clear_command = "cls" if platform.system() == "Windows" else "clear"


def clear():
    subprocess.call(clear_command, shell=True)


def print_hr(space_before=False, space_after=False):
    before = linesep if space_before else ''
    after = linesep if space_after else ''
    print(before + '-' * 80 + after)


def start(computer):
    print('Start monitoring system...')
    print_hr(space_after=True)
    # Show system info for ~16 seconds
    for _ in range(16):
        clear()
        # Display general information about computer
        print('Hostname: ' + str(computer.hostname))
        print('OS: ' + str(computer.os))
        print('CPU name: ' + str(computer.processor.name))
        print('Amount of CPU cores: ' + str(computer.processor.count))
        print('Boot time: ' + str(computer.boot_time))
        print('Uptime: ' + str(computer.uptime))
        print('Used CPU: ' + str(computer.processor.percent))
        cpu_temperature = 'unknown' if computer.processor.temperature is None else str(computer.processor.temperature)
        print('CPU temperature: ' + cpu_temperature)
        # Display memory info
        print('Nonvolatile memory: used {0} from {1}, {2}'.format(
            computer.nonvolatile_memory.available,
            computer.nonvolatile_memory.total,
            computer.nonvolatile_memory.percent
        ))
        print('Virtual memory: used {0} from {1}, {2}'.format(
            computer.virtual_memory.available,
            computer.virtual_memory.total,
            computer.virtual_memory.percent
        ))
        sleep(1)
    clear()
    # Output CPU statistic
    print('{0:_^26}_{1:_^26}_{2:_^26}'.format('Time', 'CPU load', 'CPU temperature'))
    percent_stats = computer.processor.percent_stats
    temperature_stats = computer.processor.temperature_stats
    count = max(len(percent_stats), len(temperature_stats))
    percent_stats_timetable = sorted(percent_stats)[0:count]
    temperature_stats_timetable = sorted(temperature_stats)[0:count]
    for percent_dtime, temperature_dtime in zip(percent_stats_timetable, temperature_stats_timetable):
        current_line = '{0: ^26} {1: ^26} {2: ^26}'.format(
            percent_dtime.strftime('%H:%M:%S'),
            str(percent_stats[percent_dtime]) + '%',
            str(temperature_stats[temperature_dtime]) + '°C'
        )
        print(current_line)
    print_hr(space_before=True)
    print('Shutdown monitoring system...')