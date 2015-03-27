ToolRack
========

This library is a collection of miscellaneous utility functions and classes.

`documentation <http://toolrack.readthedocs.org/>`_ |
`sources <https://bitbucket.org/ack/toolrack>`_ |
`issues <https://bitbucket.org/ack/toolrack/issues>`_


Install
-------

ToolRack can be installed from `PyPI <https://pypi.python.org/>`_.

As a user run::

  $ pip install toolrack


Development installation
------------------------

The source tree is available available at
`<https://bitbucket.com/ack/toolrack>`_, users should install `Virtualenv
<https://virtualenv.pypa.io/>`_ for development.

As a user run::

  $ virtualenv <target-dir>
  $ . <target-dir>/bin/activate
  $ git clone https://bitbucket.org/ack/toolrack.git
  $ cd toolrack
  $ python setup.py develop

Available modules
-----------------

:ref:`toolrack.convert <mod-convert>`
     Utilities for unit conversion.

:ref:`toolrack.fsmap <mod-fsmap>`
     Dict-like access to directories and contained files.

:ref:`toolrack.json_util <mod-json_util>`
     Formatting utility to indent JSON text.

:ref:`toolrack.path <mod-path>`
     Functions for searching directory trees.

:ref:`toolrack.script <mod-script>`
     A Script class to redure boilerplate when creating scripts.

:ref:`toolrack.testing <mod-testing>`
     Unit-test base classes and fixtures providing common functionalities.
