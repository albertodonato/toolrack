from pathlib import Path
from setuptools import (
    find_packages,
    setup,
)

from toolrack import (
    __doc__ as description,
    __version__,
)


tests_require = ['asynctest']

config = {
    'name': 'toolrack',
    'version': __version__,
    'license': 'LGPLv3+',
    'description': description,
    'long_description': Path('README.rst').read_text(),
    'author': 'Alberto Donato',
    'author_email': 'alberto.donato@gmail.com',
    'maintainer': 'Alberto Donato',
    'maintainer_email': 'alberto.donato@gmail.com',
    'url': 'https://github.com/albertodonato/toolrack',
    'packages': find_packages(),
    'include_package_data': True,
    'entry_points': {'console_scripts': [
        'cert-info = toolrack.scripts.certinfo:script',
        'json-indent = toolrack.scripts.json_indent:script',
        'password-generator = toolrack.scripts.password_generator:script']},
    'test_suite': 'toolrack',
    'install_requires': ['fixtures'],
    'tests_require': tests_require,
    'extras_require': {'testing': tests_require},
    'keywords': 'library utility unittest asyncio',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v3 or later (LGPLv3+)'),
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules']}

setup(**config)
