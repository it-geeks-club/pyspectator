import psutil
import platform
import os
import subprocess
import re
from .monitoring import AbcMonitor


class Processor(AbcMonitor):

    def __init__(self, monitoring_latency):
        super().__init__(monitoring_latency)
        self.__count = psutil.cpu_count()
        self.__percent = psutil.cpu_percent()
        self.__name = Processor.__get_processor_name()

    @property
    def name(self):
        return self.__name

    @property
    def count(self):
        return self.__count

    @property
    def percent(self):
        return self.__percent

    def _monitoring_action(self):
        self.__percent = psutil.cpu_percent()

    @classmethod
    def __get_processor_name(cls):
        cpu_name = None
        if platform.system() == 'Windows':
            cpu_name = platform.processor()
        elif platform.system() == 'Darwin':
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            command = 'sysctl -n machdep.cpu.brand_string'
            cpu_name = subprocess.check_output(command).strip()
        elif platform.system() == 'Linux':
            all_info = subprocess.check_output('cat /proc/cpuinfo', shell=True).strip()
            for line in all_info.split(os.linesep.encode()):
                line = line.decode()
                if 'model name' in line:
                    cpu_name = re.sub('.*model name.*:', str(), line, 1).strip()
                    break
        return cpu_name

    pass