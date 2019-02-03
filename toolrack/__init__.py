"""A collection of miscellaneous utility functions and classes."""

from distutils.version import LooseVersion

import pkg_resources

__all__ = ["__version__"]

__version__ = LooseVersion(pkg_resources.require("toolrack")[0].version)
