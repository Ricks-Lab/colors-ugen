#!/usr/bin/python3
""" setup.py used in producing source and binary distributions.

    Usage: python3 setup.py sdist bdist_wheel

    Copyright (C) 2020  RicksLab

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__author__ = 'RicksLab'
__credits__ = []
__license__ = 'GNU General Public License - GPL-3'
__program_name__ = 'setup.py'
__maintainer__ = 'RueiKe'
__docformat__ = 'reStructuredText'

# pylint: disable=line-too-long

import sys
import os
import pathlib
from setuptools import setup, find_packages
from GPUmodules import __version__, __status__

if sys.version_info < (3, 6):
    print('color_ugen requires at least Python 3.6.')
    sys.exit(1)

with open(os.path.join(pathlib.Path(__file__).parent, 'README.md'), 'r') as file_ptr:
    LONG_DESCRIPTION = file_ptr.read()

setup(name='colors_ugen',
      version=__version__,
      description='Distinct color generator',
      long_description_content_type='text/markdown',
      long_description=LONG_DESCRIPTION,
      author='RueiKe',
      keywords='colors visualization data',
      platforms='posix',
      author_email='rueikes.homelab@gmail.com',
      url='https://github.com/Ricks-Lab/colors-ugen',
      packages=find_packages(include=['CUmodules']),
      include_package_data=True,
      scripts=['color-pal'],
      license='GPL-3',
      python_requires='>=3.6',
      project_urls={'Bug Tracker':   'https://github.com/Ricks-Lab/colors-ugen/issues',
                    'Documentation': 'https://github.com/Ricks-Lab/colors-ugen/blob/master/README.md',
                    'Source Code':   'https://github.com/Ricks-Lab/colors-ugen'},
      classifiers=[__status__,
                   'Operating System :: POSIX',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3',
                   'Intended Audience :: Information Technology',
                   'Topic :: Scientific/Engineering :: Information Analysis'
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      install_requires=['matplotlib>=3.1.3'],
      data_files=[('share/colors-ugen/doc', ['README.md', 'LICENSE'])])
