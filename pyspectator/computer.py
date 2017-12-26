import platform
from datetime import datetime
import psutil
from pyspectator.monitoring import AbcMonitor
from pyspectator.memory import NonvolatileMemory, VirtualMemory, SwapMemory
from pyspectator.processor import Cpu
from pyspectator.network import NetworkInterface


class Computer(AbcMonitor):

    def __init__(self):
        self.datetime_format = '%H:%M:%S %d/%m/%Y'
        self.__raw_boot_time = psutil.boot_time()
        self.__boot_time = datetime.fromtimestamp(self.raw_boot_time)
        self.__boot_time = self.__boot_time.strftime(self.datetime_format)
        self.__hostname = platform.node()
        self.__os = Computer.__get_os_name()
        self.__architecture = platform.machine()
        self.__python_version = '{} ver. {}'.format(
            platform.python_implementation(), platform.python_version()
        )
        self.__processor = Cpu(monitoring_latency=1)
        self.__nonvolatile_memory = NonvolatileMemory.instances_connected_devices(monitoring_latency=10)
        self.__nonvolatile_memory_devices = set(
            [dev_info.device for dev_info in self.__nonvolatile_memory]
        )
        self.__virtual_memory = VirtualMemory(monitoring_latency=1)
        self.__swap_memory = SwapMemory(monitoring_latency=1)
        self.__network_interface = NetworkInterface(monitoring_latency=3)
        super().__init__(monitoring_latency=3)

    @property
    def processor(self):
        return self.__processor

    @property
    def raw_boot_time(self):
        return self.__raw_boot_time

    @property
    def boot_time(self):
        return self.__boot_time

    @property
    def raw_uptime(self):
        return datetime.now() - datetime.fromtimestamp(self.raw_boot_time)

    @property
    def uptime(self):
        return str(self.raw_uptime).split('.')[0]

    @property
    def os(self):
        return self.__os

    @property
    def architecture(self):
        return self.__architecture

    @property
    def python_version(self):
        return self.__python_version

    @property
    def hostname(self):
        return self.__hostname

    @property
    def nonvolatile_memory(self):
        return self.__nonvolatile_memory

    @property
    def virtual_memory(self):
        return self.__virtual_memory

    @property
    def swap_memory(self):
        return self.__swap_memory

    @property
    def network_interface(self):
        return self.__network_interface

    @classmethod
    def __get_os_name(cls):
        system = '{} {}'.format(platform.system(), platform.release()).strip()
        if ('Linux' in system) and ('' not in platform.linux_distribution()):
            system = ' '.join(platform.linux_distribution())
        return system

    def _monitoring_action(self):
        # Look for connected & ejected nonvolatile memory devices
        for dev in self.nonvolatile_memory:
            if not dev.is_alive:
                dev.stop_monitoring()
                self.__nonvolatile_memory_devices.remove(dev.device)
                self.__nonvolatile_memory.remove(dev)
        connected_dev = set(NonvolatileMemory.names_connected_devices()) - \
            self.__nonvolatile_memory_devices
        for dev_name in connected_dev:
            dev = NonvolatileMemory(monitoring_latency=10, device=dev_name)
            self.__nonvolatile_memory.append(dev)
            self.__nonvolatile_memory_devices.add(dev_name)

    def start_monitoring(self, all_components=True):
        super().start_monitoring()
        if all_components:
            self.processor.start_monitoring()
            for mem in self.nonvolatile_memory:
                mem.start_monitoring()
            self.virtual_memory.start_monitoring()
            self.network_interface.start_monitoring()

    def stop_monitoring(self, all_components=True):
        if all_components:
            self.processor.stop_monitoring()
            for mem in self.nonvolatile_memory:
                mem.stop_monitoring()
            self.virtual_memory.stop_monitoring()
            self.network_interface.stop_monitoring()
        super().stop_monitoring()

    def __enter__(self):
        self.start_monitoring()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_monitoring()


__all__ = ['Computer']
