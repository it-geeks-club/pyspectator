from functools import partial
from os import path


class LinuxCpuTemperatureReader():
    files = [
        '/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp',
        '/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp',
        '/sys/class/thermal/thermal_zone0/temp',
        '/proc/acpi/thermal_zone/THM0/temperature',
        '/proc/acpi/thermal_zone/THRM/temperature',
        '/proc/acpi/thermal_zone/THR1/temperature'
        
    ]

    @classmethod
    def get_reader(cls):
        readers = {
            cls.files[0]: cls.reader1,
            cls.files[1]: cls.reader1,
            cls.files[2]: cls.reader1,
            cls.files[3]: cls.reader2,
            cls.files[4]: cls.reader2,
            cls.files[5]: cls.reader2
        }
        for file in cls.files:
            if path.exists(file):
                reader = readers.get(file)
                if reader:
                    return reader(file)

    @classmethod
    def reader1(cls, file):
        def reader(file):
            temperature = float(open(file).read().strip())
            temperature = temperature / 1000
            return temperature
        return partial(reader, file)

    @classmethod
    def reader2(cls, file):
        def reader(file):
            temperature = open(file).read().strip()
            temperature = temperature.lstrip('temperature :').rstrip(' C')
            return float(temperature)
        return partial(reader, file)


class WindowsCpuTemperatureReader():

    @classmethod
    def get_reader(cls):
        import wmi
        import pythoncom

        def temperature_reader():
            pythoncom.CoInitialize()
            w = wmi.WMI(namespace='root\\wmi')
            temperature = w.MSAcpi_ThermalZoneTemperature()[0]
            temperature = float(temperature.CurrentTemperature / 10.0 - 273.15)
            return temperature
        return temperature_reader


__all__ = ['LinuxCpuTemperatureReader', 'WindowsCpuTemperatureReader']
