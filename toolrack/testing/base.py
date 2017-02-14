'''Base unit-test classes.'''

from unittest import TestCase as BaseTestCase

from fixtures import TestWithFixtures


class TestCase(TestWithFixtures, BaseTestCase):
    '''Base class for tests.'''

    def readfile(self, path):
        '''Return the content of a file.'''
        with open(path) as fd:
            return fd.read()
