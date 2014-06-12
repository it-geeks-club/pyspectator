==================
Summary
==================

pyspectator is a Python cross-platform tool for monitoring resources of OS: CPU, memory, disk, network.

==================
Requirements
==================

- OS: Linux, Windows, FreeBSD, Solaris
- Python version: 3.X
- Packages: psutil, netifaces, wmi (only on Windows), enum34 (only on python 3.0.0 - 3.4.0)

==================
How to install
==================

Run as root user:

.. code-block:: bash

    pip install pyspectator


==================
How to use
==================

You can use pyspectator as module for your own project. Simple example of usage is presented in file "console.py".

*NOTE: on Windows pyspectator can require elevated privileges. It's because Windows is fucking shit.*

Class "Computer"
------------------

.. code-block:: python

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

Class "Processor"
------------------


.. code-block:: python

    >>> from pyspectator.processor import Processor
    >>> from time import sleep
    >>> cpu = Processor(monitoring_latency=1)
    >>> with cpu:  # initiate monitoring of CPU resources
    ...     for _ in range(8):
    ...        cpu.percent, cpu.temperature
    ... 
    (8.2, 32)
    (6.6, 32)
    (6.6, 31)
    (4.1, 32)
    (5.6, 32)
    (12.3, 33)
    (4.5, 32)
    (4.5, 30)
