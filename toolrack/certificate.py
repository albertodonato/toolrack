#
# This file is part of ToolRack.
#
# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

'''Utility functions for SSL/TSL certificate handling.'''


from urllib.parse import urlsplit
from ssl import get_server_certificate


def get_host_certificate(uri, get_func=get_server_certificate):
    '''Return a string with the host certificate.

    Parameters:
        - uri: the host URI, in the form :data:`[scheme://]host[:port]`.
          The scheme is optional (and ignored), and port defaults to 443.

    '''
    split = urlsplit(uri)
    if split.scheme:
        # This is a complete URL, just take the host
        uri = split.netloc

    if ':' in uri:
        host, port = uri.split(':', maxsplit=1)
    else:
        host = uri
        port = 443
    cert = get_func((host, port))
    return cert.strip()
