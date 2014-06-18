import psutil
import platform
import os
import subprocess
import re
from collections import Callable
from datetime import datetime, timedelta
from pyspectator.monitoring import AbcMonitor
from pyspectator.collection import LimitedTimeTable


class Processor(AbcMonitor):

    # region initialization

    def __init__(self, monitoring_latency, stats_interval=None):
        super().__init__(monitoring_latency)
        self.__name = Processor.__get_processor_name()
        self.__count = psutil.cpu_count()
        self.__load = None
        self.__temperature = None
        # Init temperature reader
        self.__temperature_reader = Processor.__get_processor_temperature_reader()
        # Prepare to collect statistics
        if stats_interval is None:
            stats_interval = timedelta(hours=1)
        self.__load_stats = LimitedTimeTable(stats_interval)
        self.__temperature_stats = LimitedTimeTable(stats_interval)
        # Read updating value at first time
        self._monitoring_action()

    # endregion

    # region properties

    @property
    def name(self):
        return self.__name

    @property
    def count(self):
        return self.__count

    @property
    def load(self):
        return self.__load

    @property
    def temperature(self):
        return self.__temperature

    @property
    def load_stats(self):
        return self.__load_stats

    @property
    def temperature_stats(self):
        return self.__temperature_stats

    # endregion

    # region methods

    def _monitoring_action(self):
        now = datetime.now()
        self.__load = psutil.cpu_percent()
        self.__load_stats[now] = self.__load
        if isinstance(self.__temperature_reader, Callable):
            self.__temperature = self.__temperature_reader()
            self.__temperature_stats[now] = self.__temperature

    @classmethod
    def __get_processor_name(cls):
        cpu_name = None
        os_name = platform.system()
        if os_name == 'Windows':
            cpu_name = platform.processor()
        elif os_name == 'Darwin':
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            command = 'sysctl -n machdep.cpu.brand_string'
            cpu_name = subprocess.check_output(command).strip()
        elif os_name == 'Linux':
            all_info = subprocess.check_output('cat /proc/cpuinfo', shell=True).strip()
            for line in all_info.split(os.linesep.encode()):
                line = line.decode()
                if 'model name' in line:
                    cpu_name = re.sub('.*model name.*:', str(), line, 1).strip()
                    break
        return cpu_name

    @classmethod
    def __get_processor_temperature_reader(cls):
        reader = None
        os_name = platform.system()
        if os_name == 'Windows':
            reader = cls.__windows_processor_temperature_reader()
        elif os_name == 'Darwin':
            pass  # TODO: try to use C lib  - https://github.com/lavoiesl/osx-cpu-temp
        elif os_name == 'Linux':
            reader = cls.__linux__processor_temperature_reader()
        return reader

    # endregion

    @classmethod
    def __windows_processor_temperature_reader(cls):
        import wmi
        import pythoncom
        def temperature_reader():
            pythoncom.CoInitialize()
            w = wmi.WMI(namespace='root\\wmi')
            temperature = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature
            temperature = int(temperature / 10.0 - 273.15)
            return temperature
        return temperature_reader

    @classmethod
    def __linux__processor_temperature_reader(cls):
        reader = None

        def temperature_reader1():
            temperature = open('/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp').read().strip()
            temperature = int(temperature) // 1000
            return temperature

        def temperature_reader2():
            temperature = open('/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp').read().strip()
            temperature = int(temperature) // 1000
            return temperature

        def temperature_reader3():
            temperature = open('/proc/acpi/thermal_zone/THM0/temperature').read().strip()
            temperature = temperature.lstrip('temperature :').rstrip(' C')
            return int(temperature)

        def temperature_reader4():
            temperature = open('/proc/acpi/thermal_zone/THRM/temperature').read().strip()
            temperature = temperature.lstrip('temperature :').rstrip(' C')
            return int(temperature)

        def temperature_reader5():
            temperature = open('/proc/acpi/thermal_zone/THR1/temperature').read().strip()
            temperature = temperature.lstrip('temperature :').rstrip(' C')
            return int(temperature)

        if os.path.exists('/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp') is True:
            reader = temperature_reader1
        elif os.path.exists('/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp') is True:
            reader = temperature_reader2
        elif os.path.exists('/proc/acpi/thermal_zone/THM0/temperature') is True:
            reader = temperature_reader3
        elif os.path.exists('/proc/acpi/thermal_zone/THRM/temperature') is True:
            reader = temperature_reader4
        elif os.path.exists('/proc/acpi/thermal_zone/THR1/temperature') is True:
            reader = temperature_reader5
        return reader

    pass