from unittest import TestCase

from ..certificate import get_host_certificate


class GetHostCertificateTest(TestCase):

    def test_host_and_port(self):
        """get_host_certificate returns the host certificate."""
        remotes = []

        def fake_get_host_certificate(remote):
            remotes.append(remote)
            return 'cert'

        result = get_host_certificate(
            'https://example.com:443/resource',
            get_func=fake_get_host_certificate)
        self.assertEqual(result, 'cert')
        self.assertEqual(remotes, [('example.com', 443)])

    def test_default_port(self):
        """The default port is 443."""
        remotes = []

        def fake_get_host_certificate(remote):
            remotes.append(remote)
            return 'cert'

        result = get_host_certificate(
            'https://example.com/resource',
            get_func=fake_get_host_certificate)
        self.assertEqual(result, 'cert')
        self.assertEqual(remotes, [('example.com', 443)])

    def test_no_scheme(self):
        """An URL without scheme can be passed."""
        remotes = []

        def fake_get_host_certificate(remote):
            remotes.append(remote)
            return 'cert'

        result = get_host_certificate(
            'example.com/resource', get_func=fake_get_host_certificate)
        self.assertEqual(result, 'cert')
        self.assertEqual(remotes, [('example.com', 443)])
