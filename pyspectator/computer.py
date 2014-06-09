import psutil
import platform
from datetime import datetime
from pyspectator.monitoring import AbcMonitor
from pyspectator.memory import NonvolatileMemory, VirtualMemory, SwapMemory
from pyspectator.processor import Processor
from pyspectator.network import NetworkInterface


class Computer(AbcMonitor):

    # region initialization

    def __init__(self):
        self.datetime_format = '%H:%M:%S %d/%m/%Y'
        self.__hostname = platform.node()
        self.__os = platform.system()
        self.__python_version = '{0} ver. {1}'.format(
            platform.python_implementation(), platform.python_version()
        )
        self.__processor = Processor(monitoring_latency=1)
        self.__nonvolatile_memory = NonvolatileMemory.instances_connected_devices(monitoring_latency=10)
        self.__nonvolatile_memory_devices = set([dev_info.device for dev_info in self.__nonvolatile_memory])
        self.__virtual_memory = VirtualMemory(monitoring_latency=1)
        self.__swap_memory = SwapMemory(monitoring_latency=1)
        self.__network_interface = NetworkInterface(monitoring_latency=3)
        super().__init__(monitoring_latency=3)

    # endregion

    # region properties

    @property
    def processor(self):
        return self.__processor

    @property
    def raw_boot_time(self):
        return psutil.boot_time()

    @property
    def boot_time(self):
        return datetime.fromtimestamp(self.raw_boot_time).strftime(self.datetime_format)

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

    # endregion

    def _monitoring_action(self):
        # Look for connected & ejected nonvolatile memory devices
        for dev in self.nonvolatile_memory:
            if not dev.is_alive:
                dev.stop_monitoring()
                self.__nonvolatile_memory_devices.remove(dev.device)
                self.__nonvolatile_memory.remove(dev)
        connected_dev = set(NonvolatileMemory.names_connected_devices()) - self.__nonvolatile_memory_devices
        for dev_name in connected_dev:
            dev = NonvolatileMemory(monitoring_latency=10, device=dev_name)
            self.__nonvolatile_memory.append(dev)
            self.__nonvolatile_memory_devices.add(dev_name)

    pass
