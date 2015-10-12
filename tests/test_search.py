__author__ = 'johnthompson'
from unittest import  TestCase
from search import bestOpeningPlay, biggestPlay
from tileGroupings import Run

class TestBestOpeningPlay( TestCase ):
    def test_basic(self):
        tmp = bestOpeningPlay(['1bl','3rd','4rd','2bl','4yw','3bl','4bk'])
        self.assertEqual(len(tmp[0]), 2)
        self.assertEqual(tmp[1], ['3rd'])
        self.assertEqual(set(tmp[2]),set(['1bl','4rd','2bl','4yw','3bl','4bk'] ))



class TestBiggestPlay( TestCase ):
    def test_basic(self):
        tmp = biggestPlay(['1bl'] , [Run(['1rd','2rd', '3rd'])] )
        self.assertEqual(len(tmp[0]), 1)
        self.assertEqual(tmp[1], ['1bl'])
        self.assertEqual(tmp[2], [])

        tmp = biggestPlay(['4rd'] , [Run(['1rd','2rd', '3rd'])] )
        self.assertEqual(len(tmp[0]), 1)
        self.assertEqual(tmp[1], [])
        self.assertEqual(tmp[2], ['4rd'])