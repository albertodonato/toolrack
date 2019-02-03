"""SSL/TSL certificates info tool."""

from argparse import ArgumentParser

from ..certificate import get_host_certificate
from ..script import (
    ErrorExitMessage,
    Script,
)


class CertInfo(Script):
    """Get information about SSL certificates."""

    def get_parser(self):
        parser = ArgumentParser(description="Get information about SSL certificates.")
        subparsers = parser.add_subparsers(
            metavar="ACTION", dest="action", help="action to perform"
        )
        subparsers.required = True

        get_cert_parser = subparsers.add_parser(
            "get-cert", help="get certificate for a host"
        )
        get_cert_parser.add_argument(
            "hostname", help="hostname in the host[:port] format. Port defaults to 443"
        )
        return parser

    def main(self, args):
        action = args.action.replace("-", "_")
        method = getattr(self, "action_" + action)
        method(args)

    def action_get_cert(self, args):
        try:
            certificate = get_host_certificate(args.hostname)
        except Exception as err:
            raise ErrorExitMessage(str(err))
        else:
            print(certificate)


script = CertInfo()
