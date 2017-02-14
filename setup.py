from setuptools import setup, find_packages

from toolrack import __version__, __doc__ as description

config = {
    'name': 'toolrack',
    'version': __version__,
    'license': 'GPLv3+',
    'description': description,
    'long_description': open('README.rst').read(),
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
    'keywords': 'library utility unittest asyncio',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules']}

setup(**config)
