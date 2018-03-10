"""Base class for python scripts.

This module provides a :class:`Script` class to reduce boilerplate when
creating python scripts.

:class:`Script` instances are callable, and can optionally receive a list of
arguments (by default they look at :data:`sys.argv`).

A typical use of :class:`Script` is to declare a subclass with the script
logic and create an instance::

  class MyScript(Script):

      def main(self, args):
         # script logic here
         ...

  my_script = MyScript()

The instance can be referenced in :mod:`setuptools` ``entry_points`` key::

  setup(
      entry_points={'console_scripts': ['my_script=path.to.script:my_script']},
      ...)

"""

import sys


class ErrorExitMessage(Exception):
    """Raised to exit the process with the specified message and exit code.

    :param str message: the error message.
    :param int code: the script exit code.

    """

    def __init__(self, message, code=1):
        self.message = message
        self.code = code


class Script:
    """Wraps a python script handling argument parsing.

    Subclasses must implement :func:`get_parser` and :func:`main` methods.

    Inside :func:`main`, :exc:`ErrorExitMessage` can be raised with the
    appropriate ``message`` and ``code`` to cause the script termination, with
    the message outputted to standard error.

    Script instances are callable, and can be passed the argument list (which
    defaults to :data:`sys.argv` if not provided).

    """

    _exit = sys.exit  # For testing

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def get_parser(self):
        """Return a configured :class:`argparse.ArgumentParser` instance.

        .. note::
            Subclasses must implement this method.

        """
        raise NotImplementedError()

    def main(self, args):
        """The body of the script.

        It gets called with the :class:`argparse.Namespace` instance returned
        by :func:`get_parser`.

        :param argparse.Namespace args: command line arguments.

        .. note::
            Subclasses must implement this method.

        """
        raise NotImplementedError()

    def exit(self, code=0):
        """Exit with the specified return code."""
        self._exit(code)

    def handle_keyboard_interrupt(self, interrupt):
        """Called when a :class:`KeyboardInterrupt` is raised.

        By default it just traps the exception and exits with success.
        It can be overridden to perform additional cleanups.

        """
        self.exit()

    def __call__(self, args=None):
        """Call the script, passing :data:`sys.argv` by default."""
        parser = self.get_parser()
        parsed_args = parser.parse_args(args=args)
        try:
            self.main(parsed_args)
        except KeyboardInterrupt as interrupt:
            self.handle_keyboard_interrupt(interrupt)
        except ErrorExitMessage as error:
            self._error_exit(error)

    def _error_exit(self, error):
        """Terminate with the specified :class:`ErrorExitMessage`."""
        self._stderr.write('{}\n'.format(error.message))
        self.exit(error.code)
