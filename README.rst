=======
Summary
=======

pyspectator is a Python cross-platform tool for monitoring resources of OS: CPU, memory, disk, network.


============
Requirements
============

- OS: Linux, Windows, FreeBSD, Solaris
- Python version: 3.X
- Packages: psutil, netifaces, wmi (only on Windows), enum34 (only on python 3.0.0 - 3.4.0)

==============
How to install
==============

Run as root user:

.. code-block:: bash

    pip install pyspectator



================
Example of usage
================

There is simple project named `pyspectator_tornado <https://github.com/uzumaxy/pyspectator_tornado>`_
developed special for demonstration of pyspectator features.

.. image:: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_01_thumb.png
    :target: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_01.png
    :alt: General information

.. image:: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_02_thumb.png
    :target: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_02.png
    :alt: CPU

.. image:: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_03_thumb.png
    :target: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_03.png
    :alt: Disk devices

.. image:: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_04_thumb.png
    :target: http://uzumaxy.tk/static/img/projects/pyspectator_tornado_04.png
    :alt: Network



==========
How to use
==========

You can use pyspectator as module for your own project. Simple example of usage is presented in file "console.py".

*NOTE: on Windows pyspectator can require elevated privileges.*

Class "Computer"
----------------

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


Class "CPU"
-----------


.. code-block:: python

    >>> from pyspectator.processor import CPU
    >>> from time import sleep
    >>> cpu = CPU(monitoring_latency=1)
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
