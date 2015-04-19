#
# This file is part of ToolRack.

# ToolRack is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase

from toolrack.collect import Collection, UnknownObject, DuplicatedObject


class SampleObject(object):

    def __init__(self, name, other_attr=None):
        self.name = name
        self.other_attr = other_attr


class CollectionTests(TestCase):

    def setUp(self):
        super(CollectionTests, self).setUp()
        self.collection = Collection('SampleObject', 'name')

    def test_add(self):
        '''Objects can be added to the Collection.'''
        obj = SampleObject('foo')
        returned = self.collection.add(obj)
        self.assertIs(returned, obj)
        self.assertIs(self.collection.get('foo'), obj)

    def test_add_duplicated(self):
        '''An error is raised if the object key is already present.'''
        obj1 = SampleObject('foo')
        obj2 = SampleObject('foo')
        self.collection.add(obj1)
        self.assertRaises(DuplicatedObject, self.collection.add, obj2)

    def test_in_present(self):
        '''The key is present in the Collection'''
        self.collection.add(SampleObject('foo'))
        self.assertIn('foo', self.collection)

    def test_in_absent(self):
        '''The key is not present in the Collection'''
        self.assertNotIn('foo', self.collection)

    def test_custom_key(self):
        '''It's possible to use a different attribute as key.'''
        collection = Collection('Object', key='other_attr')
        obj = SampleObject('foo', other_attr='bar')
        collection.add(obj)
        self.assertIs(collection.get('bar'), obj)

    def test_remove(self):
        '''Objects can be removed from the Collection.'''
        obj = SampleObject('foo')
        self.collection.add(obj)
        returned = self.collection.remove('foo')
        self.assertIs(returned, obj)
        self.assertRaises(UnknownObject, self.collection.remove, 'foo')

    def test_remove_unknown(self):
        '''An error is raised if the object key is unknown.'''
        self.assertRaises(UnknownObject, self.collection.remove, 'foo')

    def test_iterable(self):
        '''The Collection is iterable.'''
        objs = [SampleObject('foo'), SampleObject('bar'), SampleObject('baz')]
        for obj in objs:
            self.collection.add(obj)
        self.assertItemsEqual(self.collection, objs)

    def test_keys(self):
        '''The Collection returns an iterable with keys.'''
        objs = [SampleObject('foo'), SampleObject('bar'), SampleObject('baz')]
        for obj in objs:
            self.collection.add(obj)
        self.assertItemsEqual(self.collection.keys(), ['foo', 'bar', 'baz'])

    def test_sorted(self):
        '''The Collection can return objects ordered by key.'''
        objs = [SampleObject('bar'), SampleObject('baz'), SampleObject('foo')]
        # Add objects in a different order.
        self.collection.add(objs[1])
        self.collection.add(objs[0])
        self.collection.add(objs[2])
        self.assertEqual(self.collection.sorted(), objs)
