__author__ = 'johnthompson'
from unittest import TestCase
from tileGroupings import RummikubPlayedSet, Run, PartialRun, Group, PartialGroup

class TestBaseClass(TestCase):
    pairs = [
        ('1bk', (1,'black')),
        ('11bk', (11, 'black')),
        ('2rd', (2, 'red')),
        ('12rd', (12, 'red')),
        ('4bl', (4, 'blue')),
        ('13bl', (13, 'blue')),
        ('5yw', (5, 'yellow')),
        ('10yw', (10, 'yellow')),
    ]

    badStrings = [
        'bk',
        '12',
        '14bl',
        '1re'
    ]
    def setUp(self):
        self.t = RummikubPlayedSet()

    def test_readTile(self):
        for pair in self.pairs:
            self.assertEqual( self.t.readTile(pair[0]), pair[1])

    def test_illPosed(self):
        for string in self.badStrings:
            with self.assertRaises(ValueError):
                self.t.readTile(string)

class TestRuns(TestCase):
    def setUp(self):
        self.run1 = Run()
        self.run2 = Run( ['5rd', '6rd', '7rd'] )
        self.run3 = Run( ['10bk', '11bk', '12bk', '13bk'])
        self.run4 = Run( ['1yw', '2yw', '3yw', '4yw', '5yw', '6yw', '7yw'])


    def test_length(self):
        self.assertEqual(len(self.run1), 0)
        self.assertEqual(len(self.run2), 3)
        self.assertEqual(len(self.run3), 4)

    def test_get_tiles(self):
        self.assertEqual( self.run1.getTiles(), None)
        self.assertEqual( self.run4.getTiles(),['1yw', '2yw', '3yw', '4yw', '5yw', '6yw', '7yw'])

    def test_equality(self):
        tmp = Run( ['5rd', '6rd','7rd', '8rd'])
        self.run2.addTile('8rd')
        self.assertEqual(self.run2, tmp)
        self.assertNotEqual(self.run2,self.run4)
        self.assertFalse(self.run2 == 'Not a run object')

        g = Group(['3bl','3rd', '3yw'])
        self.assertFalse(g == self.run2)

    def test_clone(self):
        r = self.run2.clone()
        r.addTile('8rd')
        self.assertEqual(len(self.run2), 3)

    def test_addTile(self):
        self.run2.addTile('4rd')
        self.assertEqual(len(self.run2), 4)
        self.run3.addTile('9bk')
        self.assertEqual(len(self.run3), 5)

    def test_addTile_invalid(self):
        with self.assertRaises(ValueError):
            self.run2.addTile('8bl')

        with self.assertRaises(ValueError):
            self.run3.addTile('8bk')

        with self.assertRaises(TypeError):
            self.run2.addTile(0)


    def test_addTile_too_short_on_new(self):
        with self.assertRaises(ValueError):
            self.run1.addTile(['1bl', '2bl'])

    def test_validAdds(self):
        self.assertEqual(self.run1.validAdds(), None)
        self.assertEqual(self.run2.validAdds(), ['4rd', '8rd'])
        self.assertEqual(self.run3.validAdds(), ['9bk'])
        self.assertEqual(self.run4.validAdds(), ['8yw'])
        fullRun = Run(['%dbk' %i  for i in range(1,14)])
        self.assertEqual(fullRun.validAdds(),[])

class TestPartialRun(TestCase):
    def setUp(self):
        self.run1 = PartialRun()
        self.run2 = PartialRun('1bk')
        self.run3 = PartialRun('5rd')
        self.run4 = PartialRun('13yw')

    def test_add(self):
        self.run2.addTile('2bk')
        self.assertEqual(len(self.run2), 2)

    def test_add_bad(self):
        with self.assertRaises(ValueError):
            self.run2.addTile('3bk')
        with self.assertRaises(ValueError):
            self.run2.addTile('2yw')

    def test_validAdds(self):
        self.assertEqual(self.run1.validAdds(), None)
        self.assertEqual(self.run2.validAdds(), ['2bk'])
        self.assertEqual(self.run3.validAdds(), ['4rd', '6rd'])
        self.assertEqual(self.run4.validAdds(), ['12yw'])


class TestGroup(TestCase):
    def setUp(self):
        self.group1 = Group()
        self.group2 = Group(['13bk','13bl', '13yw'])
        self.group3 = Group(['13bk','13bl', '13yw', '13rd'])


    def test_equality(self):
        self.group2.addTile('13rd')
        self.assertEqual(self.group2, self.group3)
        self.assertNotEqual(self.group1,self.group2)
        self.assertFalse(self.group2 ==  0)

        r = Run(['1bl', '2bl','3bl'])
        self.assertFalse(r == self.group2)
    def test_clone(self):
        g = self.group2.clone()
        g.addTile('13rd')
        self.assertEqual(len(self.group2),3)

    def test_get_tiles(self):
        self.assertEqual(self.group1.getTiles(), None)
        self.assertEqual(set(self.group2.getTiles()), set(['13bk','13bl', '13yw']))

    def test_length(self):
        self.assertEqual(len(self.group1), 0)
        self.assertEqual(len(self.group2), 3)
        self.assertEqual(len(self.group3), 4)

    def test_add(self):
        self.group2.addTile('13rd')
        self.assertEqual(len(self.group2), 4)

    def test_bad_add(self):
        with self.assertRaises(ValueError):
            self.group2.addTile('13bk')

        with self.assertRaises(ValueError):
            self.group2.addTile('12rd')

        with self.assertRaises(ValueError):
            self.group1.addTile(['12rd', '12yw'])

        with self.assertRaises(ValueError):
            self.group1.addTile(['12rd', '12rd', '12rd'])

        with self.assertRaises(TypeError):
            self.group2.addTile(0)

    def test_validAdds(self):
        self.assertEqual(self.group1.validAdds(), None)
        self.assertEqual(self.group2.validAdds(), ["13rd"])
        self.assertEqual(self.group3.validAdds(), [])

class TestPartialGroup(TestCase):
    def setUp(self):
        self.group1 = PartialGroup()
        self.group2 = PartialGroup('3bk')
        self.group3 = PartialGroup(['3bk', '3bl'])

    def test_addTile(self):
        self.group1.addTile('4yw')
        self.assertEqual(len(self.group1), 1)
        self.group3.addTile('3yw')
        self.assertEqual(len(self.group3), 3)

    def test_addTile_bad(self):
        with self.assertRaises(ValueError):
            self.group2.addTile('4yw')
        with self.assertRaises(ValueError):
            self.group2.addTile('3bk')

    def test_validAdds(self):
        self.assertEqual(self.group1.validAdds(), None)
        self.assertEqual(self.group2.validAdds(), ['3bl', '3rd', '3yw'])
        self.assertEqual(self.group3.validAdds(), ['3rd', '3yw'])
