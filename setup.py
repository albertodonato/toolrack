#
# This file is part of ToolRack.

# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

from toolrack import __version__, __doc__ as description


config = {
    'name': 'toolrack',
    'version': __version__,
    'license': 'GPLv3+',
    'description': description,
    'long_description': open('README.rst').read(),
    'author': 'Alberto Donato',
    'author_email': '<alberto.donato@gmail.com>',
    'maintainer': 'Alberto Donato',
    'maintainer_email': '<alberto.donato@gmail.com>',
    # 'url': '',
    # 'download_url': '',
    'packages': find_packages(exclude=['*.test.*', '*.test', 'test.*']),
    'include_package_data': True,
    # 'keywords': '',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators'
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules']}

setup(**config)
