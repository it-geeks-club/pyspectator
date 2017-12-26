from abc import ABCMeta, abstractmethod
from datetime import timedelta, datetime
import psutil
from pyspectator.monitoring import AbcMonitor
from pyspectator.collection import LimitedTimeTable


class AbsMemory(AbcMonitor, metaclass=ABCMeta):

    def __init__(self, monitoring_latency, stats_interval=None):
        # Prepare to collect statistic
        if stats_interval is None:
            stats_interval = timedelta(hours=1)
        self.__available_stats = LimitedTimeTable(stats_interval)
        self.__used_percent_stats = LimitedTimeTable(stats_interval)
        # Get info about total and available memory
        try:
            self.__total = self._get_total_memory()
            self.__available = self._get_available_memory()
            now = datetime.now()
            self.__available_stats[now] = self.available
            self.__used_percent_stats[now] = self.used_percent
        except:
            self.__total = None
            self.__available = None
            self.__available_stats.clear()
            self.__used_percent_stats.clear()
        # Init base class
        super().__init__(monitoring_latency)

    @property
    def total(self):
        return self.__total

    @property
    def available(self):
        return self.__available

    @property
    def used(self):
        used_mem = None
        if (self.total is not None) and (self.available is not None):
            used_mem = self.total - self.available
        return used_mem

    @property
    def used_percent(self):
        percent = None
        used = self.used
        if used is not None:
            percent = int(used / self.total * 100)
        return percent

    @property
    def available_stats(self):
        return self.__available_stats

    @property
    def used_percent_stats(self):
        return self.__used_percent_stats

    def _monitoring_action(self):
        try:
            self.__available = self._get_available_memory()
            now = datetime.now()
            self.__available_stats[now] = self.available
            self.__used_percent_stats[now] = self.used_percent
        except:
            self.__available = None
            self.__available_stats.clear()
            self.__used_percent_stats.clear()
            self.stop_monitoring()

    @abstractmethod
    def _get_total_memory(self):
        raise NotImplementedError('Method not implemented by derived class!')

    @abstractmethod
    def _get_available_memory(self):
        raise NotImplementedError('Method not implemented by derived class!')


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

    def __init__(self, monitoring_latency, device):
        dev_info = None
        for current_dev_info in psutil.disk_partitions():
            if current_dev_info.device == device:
                dev_info = current_dev_info
                break
        if dev_info is None:
            raise DeviceNotFoundException(
                'Device {} not found!'.format(device)
            )
        self.__is_alive = True
        self.__device = device
        self.__mountpoint = dev_info.mountpoint
        self.__fstype = dev_info.fstype
        super().__init__(monitoring_latency)

    @property
    def device(self):
        return self.__device

    @property
    def mountpoint(self):
        return self.__mountpoint

    @property
    def fstype(self):
        return self.__fstype

    @property
    def is_alive(self):
        return self.__is_alive

    def _get_available_memory(self):
        return psutil.disk_usage(self.mountpoint).free

    def _get_total_memory(self):
        return psutil.disk_usage(self.mountpoint).total

    def _monitoring_action(self):
        devices = NonvolatileMemory.names_connected_devices()
        self.__is_alive = self.device not in devices
        if self.is_alive:
            super()._monitoring_action()

    @staticmethod
    def instances_connected_devices(monitoring_latency):
        devices = list()
        for current_dev_info in psutil.disk_partitions():
            current_dev = NonvolatileMemory(
                monitoring_latency, current_dev_info.device
            )
            devices.append(current_dev)
        return devices

    @staticmethod
    def names_connected_devices():
        return [dev_info.device for dev_info in psutil.disk_partitions()]


class DeviceNotFoundException(Exception):
    pass


__all__ = [
    'AbsMemory',
    'VirtualMemory',
    'SwapMemory',
    'NonvolatileMemory',
    'DeviceNotFoundException'
]
