__author__ = 'johnthompson'
from sys import argv
from tileGroupings import getGrouping
from search import biggestPlay

if __name__ == '__main__':
    if len(argv) != 3:
        print "%s <table_file> <rack_file>" % argv[0]
        exit(1)

    table = []
    FH = open(argv[1])
    for line in FH.readlines():
        tiles = [i.strip() for i in line.split(",") if len(i.strip()) > 0]
        if len(tiles) == 0:
            continue
        table.append(getGrouping(tiles))
    FH.close()

    FH = open(argv[2])
    rack = [i.strip() for i in FH.readline().split(',')]

    new_table, remaing_rack, used_tiles = biggestPlay(rack, table)

    print "New Table:"
    for i in new_table:
        print i
    print
    print "New Rack:"
    print ", ".join(remaing_rack)
    print
    print "Used tiles:"
    print ", ".join(used_tiles)