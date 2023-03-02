"""Utility functions for SSL/TSL certificate handling."""

from collections.abc import Callable
from ssl import get_server_certificate
from urllib.parse import urlsplit


def get_host_certificate(
    uri: str, get_func: Callable[[tuple[str, int]], str] = get_server_certificate
) -> str:
    """Return a string with the host certificate.

    :param str uri: the host URI, in the form :data:`[scheme://]host[:port]`.
        The scheme is optional (and ignored), and port defaults to 443.

    """
    split = urlsplit(uri)
    if split.scheme:
        # This is a complete URL, just take the host
        uri = split.netloc
    else:
        uri, _ = uri.split("/", 1)

    if ":" in uri:
        host, port = uri.split(":", maxsplit=1)
        int_port = int(port)
    else:
        host = uri
        int_port = 443
    cert = get_func((host, int_port))
    return cert.strip()
