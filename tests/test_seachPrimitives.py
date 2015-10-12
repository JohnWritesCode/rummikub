__author__ = 'johnthompson'
from unittest import TestCase
from searchPrimitives import  findPlays
from tileGroupings import Run, Group

class TestFindPlays(TestCase):

    def test_starting_plays(self):
        tmp = findPlays(['1bl', '2bl', '3bl', '6rd'])
        self.assertEqual(len(tmp[0]), 1)
        self.assertEqual(tmp[0][0], Run(['1bl', '2bl', '3bl']))
        self.assertEqual(tmp[1], ['6rd'])
        tmp = findPlays(['1bl', '2bl', '3bl', '4bl', '5bl', '3rd','3yw'])
        self.assertEqual(len(tmp[0]), 1)
        self.assertEqual(len(tmp[1]), 2) ## that it created the run, not the group


        tmp= findPlays(['1bl','1bk','1rd','1yw'])
        self.assertEqual(len(tmp[0]), 1)
        self.assertEqual(len(tmp[0][0]), 4)
        self.assertEqual(len(tmp[1]), 0)

        tmp = findPlays(['1bl', '2bl', '3bl', '4bl', '5bl', '3rd','3yw','3bk'])
        self.assertEqual(len(tmp[0]), 2)
        self.assertEqual(len(tmp[1]), 0) ## that it created the run, not the group

        tmp = findPlays(['1bl','2bl', '3bl', '1rd', '2rd', '3rd', '1yw','2yw','3yw'])
        self.assertEqual(len(tmp[0]), 3)
        self.assertEqual(len(tmp[1]), 0)

        tmp = findPlays(['1bl','2bl', '3bl', '1rd', '2rd', '3rd', '1yw','2yw','3yw', '12bl','12rd', '12bk', '13rd'])
        self.assertEqual(len(tmp[0]), 4)
        self.assertEqual(len(tmp[1]), 1)

        tmp = findPlays(['1bl','2bl','3bl','4bl','5bl','6bl', '7bl', '4yw', '4rd'])
        self.assertEqual(len(tmp[0]), 3)
        self.assertEqual(len(tmp[1]), 0) ## make two runs and a group instead of a big run and dangling tiles


    def test_required_tiles(self):
        tmp = findPlays(['1bl', '2bl', '3bl'], None, ['1bl','2bl','3bl'])
        self.assertEqual(len(tmp[0]),1)
        self.assertEqual(len(tmp[1]), 0)

        tmp = findPlays(['1bl', '2bl', '3bl', '4bl'], None, ['1bl','2bl','3bl'])
        self.assertEqual(len(tmp[0]),1)
        self.assertEqual(len(tmp[1]), 0)

        tmp = findPlays(['1bl', '2bl', '3rd', '4bl'], None, ['1bl','2bl','4bl'])
        self.assertEqual(tmp[0], None)
        self.assertEqual(tmp[1], None)

        tmp = findPlays(['1bl', '2bl','3bl','4bl','5bl', '3rd','3yw'], None, ['3bl','3rd','3yw'])
        self.assertEqual(len(tmp[0]),1)
        self.assertEqual(len(tmp[1]), 4) ## can't break up the group of 3s, even though that would use more tiles

