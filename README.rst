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

:mod:`toolrack.convert`
     Utilities for unit conversion.

:mod:`toolrack.fsmap`
     Dict-like access to directories and contained files.

:mod:`toolrack.json_util`
     Formatting utility to indent JSON text.

:mod:`toolrack.path`
     Functions for searching directory trees.

:mod:`toolrack.script`
     A Script class to redure boilerplate when creating scripts.

:mod:`toolrack.testing`
     Unit-test base classes and fixtures providing common functionalities.
