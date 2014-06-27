import sys
import platform
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def main():
    # Check python version
    if sys.version_info < (3, 0, 0):
        sys.stderr.write('You need python 3.0 or later to run this script!' + os.linesep)
        exit(1)
    # Generate requires
    requires = [
        "psutil >= 2.1.1",
        "netifaces >= 0.10.4",
    ]
    if sys.version_info < (3, 4, 1):
        requires.append("enum34 >= 1.0")
    if platform.system() == 'Windows':
        requires.append('wmi >= 1.4.9')
    # Describe installer
    setup(
        name='pyspectator',
        version='1.0.8',
        author='Maxim Grischuk, Vova Sirenko',
        author_email='uzumaxy@gmail.com',
        maintainer='Maxim Grischuk',
        maintainer_email='uzumaxy@gmail.com',
        packages=['pyspectator'],
        url='https://github.com/opium999/pyspectator',
        download_url='https://github.com/opium999/pyspectator/releases',
        license='BSD',
        description='pyspectator is a cross-platform tool for retrieving full information about computer.',
        long_description=open('README.rst').read(),
        install_requires=requires,
        keywords=[
            'pyspectator', 'spectator',
            'monitoring', 'tool',
            'statistic', 'stats',
            'computer', 'pc', 'server',
            'mem', 'memory',
            'network', 'net', 'io',
            'processor', 'cpu',
            'hdd', 'hard', 'disk', 'drive'
        ],
        platforms='Platform Independent',
        package_data={
            'pyspectator': ['LICENSE', 'README.rst']
        },
        scripts=['console.py'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows :: Windows 7',
            'Operating System :: Microsoft :: Windows :: Windows NT/2000',
            'Operating System :: Microsoft :: Windows :: Windows Server 2003',
            'Operating System :: Microsoft :: Windows :: Windows Server 2008',
            'Operating System :: Microsoft :: Windows :: Windows Vista',
            'Operating System :: Microsoft :: Windows :: Windows XP',
            'Operating System :: Microsoft',
            'Operating System :: OS Independent',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: SunOS/Solaris',
            'Operating System :: POSIX',
            'Programming Language :: C',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: System :: Benchmark',
            'Topic :: System :: Hardware',
            'Topic :: System :: Monitoring',
            'Topic :: System :: Networking :: Monitoring',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
        ],
    )


if __name__ == '__main__':
    main()