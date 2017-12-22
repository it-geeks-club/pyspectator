import sys
import platform
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = list()

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = list()
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        err_no = pytest.main(self.pytest_args)
        sys.exit(err_no)


def main():
    # Check python version
    if sys.version_info < (3, 0, 0):
        sys.stderr.write(
            'You need python 3.0 or later to run this script!' + os.linesep
        )
        exit(1)
    # Generate requires
    if platform.system() == 'Windows':
        requirements_file = 'windows.txt'
    else:
        requirements_file = 'base.txt'
    requirements_file = os.path.join('requirements', requirements_file)
    with open(requirements_file) as fd:
        requires = fd.read().splitlines()
    # Get package description
    with open('README.rst') as fd:
        long_description = fd.read()
    # Describe installer
    settings = {
        'name': 'pyspectator',
        'version': '1.2.1',
        'author': 'Maxim Grischuk',
        'author_email': 'uzumaxy@gmail.com',
        'maintainer': 'Maxim Grischuk',
        'maintainer_email': 'uzumaxy@gmail.com',
        'packages': ['pyspectator'],
        'url': 'https://github.com/it-geeks-club/pyspectator',
        'download_url': 'https://github.com/it-geeks-club/pyspectator/releases',
        'license': 'BSD',
        'description': 'pyspectator is a Python cross-platform tool for '
                       'monitoring OS resources.',
        'long_description': long_description,
        'install_requires': requires,
        'keywords': [
            'pyspectator', 'spectator',
            'monitoring', 'tool',
            'statistic', 'stats',
            'computer', 'pc', 'server',
            'mem', 'memory',
            'network', 'net', 'io',
            'processor', 'cpu',
            'hdd', 'hard', 'disk', 'drive'
        ],
        'platforms': 'Platform Independent',
        'package_data': {
            'pyspectator': ['LICENSE', 'README.rst']
        },
        'scripts': ['console.py'],
        'tests_require': ['pytest'],
        'cmdclass': {'test': PyTest},
        'classifiers': [
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
            'Programming Language :: Python :: 3.5',
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
    }
    setup(**settings)


if __name__ == '__main__':
    main()
