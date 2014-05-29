__author__ = 'uzumaxy'

import psutil
from threading import Timer
from abc import ABCMeta, abstractmethod


class AbsMemory(metaclass=ABCMeta):

    # region initialization

    def __init__(self, monitoring_latency):
        self.__total = self._get_total_memory()
        self.__available = self._get_available_memory()
        self.__monitoring_latency = None
        self.monitoring_latency = monitoring_latency
        self.__monitoring = False

    # endregion

    # region properties

    @property
    def monitoring(self):
        return self.__monitoring

    @property
    def monitoring_latency(self):
        return self.__monitoring_latency

    @monitoring_latency.setter
    def monitoring_latency(self, value):
        self.__monitoring_latency = value

    @property
    def total(self):
        return self.__total

    @property
    def available(self):
        return self.__available

    @property
    def percent(self):
        _percent = (self.total - self.available) / self.total
        _percent = '{:.2%}'.format(_percent)
        return _percent

    # endregion

    # region methods

    def start_monitoring(self):
        if self.__monitoring is False:
            self.__monitoring = True
            self.__monitoring_action()

    def stop_monitoring(self):
        self.__monitoring = False

    def __monitoring_action(self):
        if self.__monitoring is True:
            self.__available = self._get_available_memory()
            Timer(self.monitoring_latency, self.__monitoring_action).start()

    # endregion

    # region abstract methods

    @abstractmethod
    def _get_total_memory(self):
        raise NotImplementedError('Method not implemented by derived class!')

    @abstractmethod
    def _get_available_memory(self):
        raise NotImplementedError('Method not implemented by derived class!')

    # endregion

    pass


class VirtualMemory(AbsMemory):

    def __init__(self, monitoring_latency):
        super().__init__(monitoring_latency)

    def _get_available_memory(self):
        return psutil.virtual_memory().available

    def _get_total_memory(self):
        return psutil.virtual_memory().total


class SwapMemory(AbsMemory):

    def __init__(self, monitoring_latency):
        super().__init__(monitoring_latency)

    def _get_available_memory(self):
        return psutil.swap_memory().free

    def _get_total_memory(self):
        return psutil.swap_memory().total


class NonvolatileMemory(AbsMemory):

    def __init__(self, monitoring_latency):
        super().__init__(monitoring_latency)

    def _get_available_memory(self):
        return psutil.disk_usage('/').free

    def _get_total_memory(self):
        return psutil.disk_usage('/').total