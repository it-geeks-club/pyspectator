# Summary

pyspectator is a Python cross-platform tool for monitoring resources of OS: CPU, memory, disk, network.

# Requirements

* OS: Linux, Windows, FreeBSD, Solaris
* Python version: 3.X
* Packages: psutil, netifaces, wmi (only on Windows), enum34 (only on python 3.0.0 - 3.4.0)

# How to install

* With PyPi: `pip install -U pyspectator`  
* Manually: `python setup.py install`



# Example of usage

There is simple project named [pyspectator_tornado](https://github.com/uzumaxy/pyspectator_tornado) developed special for demonstration of pyspectator features.

[![General information](http://i.imgur.com/yUjNlyQ.png)](http://i.imgur.com/LFMmfHu.png)

[![CPU](http://i.imgur.com/omNJhno.png)](http://i.imgur.com/r0RuV2m.png)

[![Disk devices](http://i.imgur.com/qc3NwBa.png)](http://i.imgur.com/zA7mteS.png)

[![Network](http://i.imgur.com/Dugsnr6.png)](http://i.imgur.com/rDadDzn.png)


# How to use

You can use pyspectator as module for your own project. Simple example of usage is presented in file `console.py`.

_NOTE: on Windows pyspectator can require elevated privileges._

## Class "Computer"

    >>> from pyspectator.computer import Computer
    >>> computer = Computer()
    >>> computer.os
    'Linux 3.14.4-1-MANJARO'
    >>> computer.python_version
    'CPython ver. 3.4.1'
    >>> computer.uptime
    '1:07:52'
    >>> computer.processor.name
    'Intel(R) Core(TM) i3-3110M CPU @ 2.40GHz'


## Class "Cpu"

    >>> from pyspectator.processor import Cpu
    >>> from time import sleep
    >>> cpu = Cpu(monitoring_latency=1)
    >>> with cpu:
    ...     for _ in range(8):
    ...        cpu.load, cpu.temperature
    ...        sleep(1.1)
    ...
    (22.6, 55)
    (6.1, 55)
    (5.5, 54)
    (7.1, 54)
    (5.6, 54)
    (7.0, 54)
    (10.2, 54)
    (6.6, 54)

