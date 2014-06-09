from distutils.core import setup
import platform


def main():
    requires = [
        "psutil >= 2.1.1",
        "netifaces >= 0.10.4",
    ]
    if platform.system() == 'Windows':
        requires.append('wmi >= 1.4.9')
    description = 'pyspectator is a cross-platform library for retrieving full information about computer.'
    setup(
        name='pyspectator',
        version='1.0.1',
        author='Maxim Grischuk, Vova Sirenko',
        author_email='uzumaxy@gmail.com',
        packages=['pyspectator'],
        url='https://github.com/opium999/pyspectator',
        download_url='https://github.com/opium999/pyspectator/releases',
        license='BSD',
        description=description,
        long_description=description,
        install_requires=requires,
        keywords=['spectator', 'monitoring', 'statistic', 'mem', 'network', 'io', 'cpu', 'disk'],
        platforms='Platform Independent',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows :: Windows NT/2000',
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