import subprocess
import platform
from os import linesep
from time import sleep
from pyspectator.convert import UnitByte


CLEAR_CMD = 'cls' if platform.system() == 'Windows' else 'clear'


def clear():
    subprocess.call(CLEAR_CMD, shell=True)


def print_hr(space_before=False, space_after=False):
    before = linesep if space_before else ''
    after = linesep if space_after else ''
    print(before + '-' * 80 + after)


class Format(object):

    @staticmethod
    def temperature(value):
        formatted_value = ''
        if isinstance(value, (int, float)):
            formatted_value = str(value) + '°C'
        return formatted_value

    @staticmethod
    def byte_value(value):
        formatted_value = ''
        if isinstance(value, (int, float)):
            value, unit = UnitByte.auto_convert(value)
            value = '{:.2f}'.format(value)
            unit = UnitByte.get_name_reduction(unit)
            formatted_value = value + unit
        return formatted_value

    @staticmethod
    def percent(value):
        formatted_value = ''
        if isinstance(value, (int, float)):
            formatted_value = str(value) + '%'
        return formatted_value


def main(computer):
    print('Start monitoring system...')
    print_hr(space_after=True)
    # Show system info for ~16 seconds
    for _ in range(16):
        clear()
        # Display general information about computer
        print('OS: ' + str(computer.os))
        print('Boot time: {}; Uptime: {}'.format(
            computer.boot_time, computer.uptime
        ))
        print('')
        # Display CPU info
        print('CPU name: ' + str(computer.processor.name))
        print('Amount of CPU cores: ' + str(computer.processor.count))
        print('CPU load: ' + Format.percent(computer.processor.load))
        cpu_temperature = 'unknown'
        if computer.processor.temperature is not None:
            cpu_temperature = Format.temperature(
                computer.processor.temperature
            )
        print('CPU temperature: ' + cpu_temperature)
        print('')
        # Display network info
        print('Hostname: ' + str(computer.hostname))
        print('Network interface: ' + str(computer.network_interface.name))
        print('MAC: ' + str(computer.network_interface.hardware_address))
        print('IP: {}; Mask: {}; Gateway: {}'.format(
            computer.network_interface.ip_address,
            computer.network_interface.subnet_mask,
            computer.network_interface.default_route
        ))
        print('Sent data: {}; Received data: {}'.format(
            Format.byte_value(computer.network_interface.bytes_sent),
            Format.byte_value(computer.network_interface.bytes_recv)
        ))
        print('')
        # Display virtual memory info
        print('Virtual memory: use {} from {}, {}'.format(
            Format.byte_value(computer.virtual_memory.available),
            Format.byte_value(computer.virtual_memory.total),
            Format.percent(computer.virtual_memory.used_percent)
        ))
        print('')
        # Display nonvolatile memory info
        output_format1 = '{:_^16}{:_^16}{:_^16}{:_^16}{:_^16}'
        output_format2 = '{: ^16}{: ^16}{: ^16}{: ^16}{: ^16}'
        print(output_format1.format('Device', 'Total', 'Use', 'Type', 'Mount'))
        for dev in computer.nonvolatile_memory:
            output_text = output_format2.format(
                dev.device,
                Format.byte_value(dev.total),
                Format.percent(dev.used_percent),
                dev.fstype,
                dev.mountpoint
            )
            print(output_text)
        sleep(1)
    print_hr(space_before=True)
    print('Shutdown monitoring system...')


if __name__ == '__main__':
    # Initialize computer instance
    from pyspectator.computer import Computer
    COMPUTER = Computer()
    # Start monitoring system
    with COMPUTER:
        # Start console interface
        main(COMPUTER)
