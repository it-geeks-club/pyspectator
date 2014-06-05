import psutil
import platform
from datetime import datetime
from .memory import NonvolatileMemory, VirtualMemory, SwapMemory
from .processor import Processor


class Computer(object):

    # region initialization

    def __init__(self):
        self.datetime_format = '%H:%M:%S %d/%m/%Y'
        self.__hostname = platform.node()
        self.__os = platform.system()
        self.__python_version = '{0} ver. {1}'.format(
            platform.python_implementation(), platform.python_version()
        )
        self.__processor = Processor(monitoring_latency=1)
        self.__nonvolatile_memory = NonvolatileMemory.connected_devices(monitoring_latency=10)
        self.__virtual_memory = VirtualMemory(monitoring_latency=1)
        self.__swap_memory = SwapMemory(monitoring_latency=3)

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

    # endregion

    pass
