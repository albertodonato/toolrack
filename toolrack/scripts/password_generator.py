"""Generate random passwords."""

from argparse import ArgumentParser
from collections import OrderedDict

from ..password import (
    DEFAULT_LENGTH,
    PasswordProfile,
)
from ..script import Script

PROFILES = OrderedDict(
    [
        ("default", PasswordProfile("{alnum}-_/")),
        ("allchars", PasswordProfile("{alnum}{punct}")),
    ]
)


class PasswordGenerator(Script):
    """Script to generate random passwords."""

    def get_parser(self):
        parser = ArgumentParser(description="Generate random passwords")
        parser.add_argument(
            "-n", type=int, default=1, help="number of passwords to generate"
        )
        parser.add_argument(
            "-l", "--length", type=int, default=DEFAULT_LENGTH, help="password length"
        )
        parser.add_argument(
            "-p",
            "--profile",
            default="default",
            help=(
                "profile to use. Can be the name of a defined profile or a "
                "sequence of character definitions."
            ),
        )
        parser.add_argument(
            "-L", "--list-profiles", action="store_true", help="list available profiles"
        )
        parser.add_argument(
            "-d", "--list-defs", action="store_true", help="list characters definitions"
        )
        return parser

    def main(self, args):
        if args.list_profiles:
            self._list_profiles()
            self.exit()

        if args.list_defs:
            self._list_definitions()
            self.exit()

        if args.profile in PROFILES:
            profile = PROFILES[args.profile]
        else:
            profile = PasswordProfile(args.profile)

        for _ in range(args.n):
            password = profile.generate(length=args.length)
            print(password)

    def _list_profiles(self):
        """List available profiles."""
        for name, profile in PROFILES.items():
            message = "{}:\n  definition: {}\n  characters: {}"
            print(message.format(name, profile.definition, profile.chars))

    def _list_definitions(self):
        """List available character set definitions."""
        for tag, chars in PasswordProfile.CHAR_DEFS.items():
            print(f"{tag}: {chars!r}")


script = PasswordGenerator()
