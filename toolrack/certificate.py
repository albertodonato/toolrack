"""Utility functions for SSL/TSL certificate handling."""

from urllib.parse import urlsplit
from ssl import get_server_certificate


def get_host_certificate(uri, get_func=get_server_certificate):
    """Return a string with the host certificate.

    :param str uri: the host URI, in the form :data:`[scheme://]host[:port]`.
        The scheme is optional (and ignored), and port defaults to 443.

    """
    split = urlsplit(uri)
    if split.scheme:
        # This is a complete URL, just take the host
        uri = split.netloc
    else:
        uri, _ = uri.split('/', 1)

    if ':' in uri:
        host, port = uri.split(':', maxsplit=1)
        port = int(port)
    else:
        host = uri
        port = 443
    cert = get_func((host, port))
    return cert.strip()
