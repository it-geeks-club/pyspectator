__author__ = 'uzumaxy'

import psutil
import platform
from .memory import NonvolatileMemory, VirtualMemory, SwapMemory


class Computer(object):

    # region initialization

    def __init__(self):
        self.__hostname = platform.node()
        self.__os = platform.system()
        self.__python_version = '{0} ver. {1}'.format(
            platform.python_implementation(), platform.python_version()
        )
        self.__nonvolatile_memory = NonvolatileMemory(monitoring_latency=10)
        self.__virtual_memory = VirtualMemory(monitoring_latency=1)
        self.__swap_memory = SwapMemory(monitoring_latency=3)

    # endregion

    # region properties

    @property
    def boot_time(self):
        return psutil.boot_time()

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
