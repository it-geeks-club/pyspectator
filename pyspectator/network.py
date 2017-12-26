import socket
from datetime import timedelta, datetime
import psutil
import netifaces as nif
from pyspectator.monitoring import AbcMonitor
from pyspectator.collection import LimitedTimeTable


class NetworkInterface(AbcMonitor):

    def __init__(self, monitoring_latency, stats_interval=None,
                 ip_address=None):
        super().__init__(monitoring_latency)
        self.__name = None
        self.__hardware_address = None
        if ip_address is None:
            ip_address = NetworkInterface.__get_active_ip_address()
        self.__ip_address = ip_address
        self.__broadcast_address = None
        self.__subnet_mask = None
        self.__default_route = None
        self.__bytes_sent = 0
        self.__bytes_recv = 0
        # Get interface name, network mask and broadcast address
        if self.__ip_address is not None:
            for interface in nif.interfaces():
                addresses = nif.ifaddresses(interface)
                try:
                    af_inet = addresses[nif.AF_INET][0]
                    if af_inet['addr'] != self.__ip_address:
                        continue
                    af_link = addresses[nif.AF_LINK][0]
                    self.__name = NetworkInterface.__check_interface_name(
                        interface
                    )
                    self.__hardware_address = af_link['addr']
                    self.__broadcast_address = af_inet['broadcast']
                    self.__subnet_mask = af_inet['netmask']
                    break
                except (IndexError, KeyError):
                    # ignore interfaces, which don't have MAC or IP
                    continue
        # Get gateway address
        if self.name is not None:
            for gateway_info in nif.gateways()[nif.AF_INET]:
                if self.name in gateway_info:
                    self.__default_route = gateway_info[0]
                    break
        # Prepare to collect statistics
        if stats_interval is None:
            stats_interval = timedelta(hours=1)
        self.__bytes_sent_stats = LimitedTimeTable(stats_interval)
        self.__bytes_recv_stats = LimitedTimeTable(stats_interval)
        # Read updating values at first time
        self._monitoring_action()

    @property
    def name(self):
        return self.__name

    @property
    def hardware_address(self):
        return self.__hardware_address

    @property
    def ip_address(self):
        return self.__ip_address

    @property
    def broadcast_address(self):
        return self.__broadcast_address

    @property
    def subnet_mask(self):
        return self.__subnet_mask

    @property
    def default_route(self):
        return self.__default_route

    @property
    def bytes_sent(self):
        return self.__bytes_sent

    @property
    def bytes_recv(self):
        return self.__bytes_recv

    @property
    def bytes_sent_stats(self):
        return self.__bytes_sent_stats

    @property
    def bytes_recv_stats(self):
        return self.__bytes_recv_stats

    @classmethod
    def __check_interface_name(cls, name):
        net_io = psutil.net_io_counters(pernic=True)
        if name in net_io:
            return name
        for curr_nif_name in net_io:
            if name in curr_nif_name:
                name = curr_nif_name
                break
        return name

    @classmethod
    def __get_active_ip_address(cls):
        ip_address = None
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip_address = s.getsockname()[0]
        except:
            s.close()
        return ip_address

    def _monitoring_action(self):
        net_io = psutil.net_io_counters(pernic=True)
        if self.name in net_io:
            net_io = net_io[self.name]
            now = datetime.now()
            self.__bytes_sent = net_io.bytes_sent
            self.__bytes_recv_stats[now] = self.bytes_sent
            self.__bytes_recv = net_io.bytes_recv
            self.__bytes_recv_stats[now] = self.bytes_recv


__all__ = ['NetworkInterface']
