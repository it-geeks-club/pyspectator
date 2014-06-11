pyspectator
===========

Cross-platform tool for monitoring resources of OS with web-interface.

How to install
===========

Run as root user:
```bash
pip install pyspectator
```

Requirements
===========

- Python version: 3.X
- Packages: psutil, netifaces, wmi (only on Windows), enum34 (only on python 3.0.0 - 3.4.0)

How to use
===========

You can use pyspectator as module for your own project. Simple example of usage is presented in file "console.py".

*NOTE: on Windows pyspectator can require elevated privileges. It's because Windows is fucking shit.*
