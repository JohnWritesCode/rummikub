__author__ = 'johnthompson'
import re

class RummikubPlayedSet(object):
    tileRE = re.compile(r'(\d{1,2})(\w{2})')
    colorMap = {
        "bk": "black",
        "bl": "blue",
        "rd": "red",
        "yw": "yellow",
    }

    abbrevMap = {
        "black": "bk",
        "blue": 'bl',
        "red": "rd",
        "yellow": "yw",
    }

    def __init__(self, tiles = None):
        if tiles != None:
            self.addTile(tiles)


    def readTile(self, tileStr):
        m = self.tileRE.search(tileStr)
        if m == None:
            raise ValueError("string '%s' is not a valid tile string" % tileStr)
        number = int(m.group(1))
        color = m.group(2)
        if not 1 <= number <= 13:
            raise ValueError("tile number must be between 1 and 13 (got '%s')" % tileStr)
        if not color in self.colorMap.keys():
            raise ValueError("color must be one of " + str(self.colorMap.keys()) + "got '%s'" % tileStr)
        return (number, self.colorMap[color])


class Run(RummikubPlayedSet):
    color = None
    start = None
    end = None


    def __len__(self):
        if self.color == None:
            return 0
        else:
            return self.end - self.start + 1 # +1 since our ends are both inclusive

    def __str__(self):
        if self.color == None:
            return "Unitialized Run"
        else:
            return ','.join(['%d%s' % (i, self.abbrevMap[self.color]) for i in range(self.start, self.end+1)])


    def __eq__(self, other):
        try:
            return self.color == other.color and self.start == other.start and self.end == other.end
        except AttributeError: # other item isn't a run
            return False

    def clone(self):
        out = Run()
        out.color = self.color
        out.start = self.start
        out.end = self.end
        return out

    def addTile(self, tile):
        if type(tile) == str:
            if self.color == None:
                raise ValueError("can only provide single input to initialized run")
            number, color = self.readTile(tile)
            if color != self.color:
                raise ValueError("color mismatch. Run color is '%s' got '%s'" % (self.color, tile))
            if number == self.start -1:
                self.start -= 1
            elif number == self.end + 1:
                self.end +=1
            else:
                raise ValueError("number was not in set. Current start and end are (%d,%d) got '%s'" % (self.start, self.end, tile))
        elif type(tile) in (list, tuple):
            if len(tile) < 3 and self.color == None:
                raise ValueError("need at least 3 elements to initialize a Run")
            for entry in tile:
                if self.color == None:
                    number, color = self.readTile(entry)
                    self.color = color
                    self.start = number
                    self.end = number
                else:
                    self.addTile(entry)

        else:
            raise TypeError("must provide addTile with string or list (got '%s')" % str(tile))

    def validAdds(self):
        if self.color == None:
            return None
        out = []
        if self.start > 1:
            out.append("%d%s" % (self.start-1, self.abbrevMap[self.color]))
        if self.end < 13:
            out.append("%d%s" % (self.end + 1, self.abbrevMap[self.color]))
        return out

class PartialRun(Run):
    def addTile(self, tile):
        if type(tile) != str:
            raise ValueError("Partial run only supports adding a single tile")
        number, color = self.readTile(tile)
        if self.color == None:
            self.color = color
            self.start = number
            self.end = number
        elif self.color != color:
            raise ValueError("entry '%s' does not match color '%s'" % (tile, self.color))
        else:
            if number == self.end +1:
                self.end += 1
            elif number == self.start -1:
                self.start -= 1
            else:
                raise ValueError("entry '%s' is not next in series '%s'" % (tile, str(self)))


class Group(RummikubPlayedSet):
    number = None
    missingColors = None

    def __str__(self):
        if self.number == None:
            return "Unintialized Group"
        else:
            outList = []
            for color in self.colorMap.values():
                if color not in self.missingColors:
                    outList.append( '%d%s' % (self.number, self.abbrevMap[color]) )

            return ','.join(outList)

    def __eq__(self, other):
        try:
            return self.number == other.number and self.missingColors == other.missingColors
        except AttributeError: ## the other objects isn't a group
            return False


    def clone(self):
        out = Group()
        out.number = self.number
        out.missingColors = self.missingColors[:]
        return out


    def __init_missing_colors__(self):
        self.missingColors = self.colorMap.values()

    def __add_single_tile__(self, tile):
        number, color =  self.readTile(tile)
        if self.number == None:
            self.number = number
        elif self.number != number:
            raise ValueError("tile '%s' does not match group  '%s'" % (tile, str(self)))
        if self.missingColors == None:
            self.__init_missing_colors__()
        elif color not in self.missingColors:
            raise ValueError("tile '%s' was already in group '%s'" % (tile, str(self)))
        self.missingColors.remove(color)


    def addTile(self, tile):
        if type(tile) == str:
            if self.number == None:
                raise ValueError("can only input single tile to initialized group")
            self.__add_single_tile__(tile)
        elif type(tile) in (list, tuple):
            if len(tile) not in (3,4):
                raise ValueError("a group must be 3 or 4 long. Got '%s'" % str(tile))
            for t in tile:
                self.__add_single_tile__(t)
        else:
            raise TypeError("must provide addTile with string or list")

    def __len__(self):
        if self.number == None:
            return 0
        else:
            return 4 - len(self.missingColors)

    def validAdds(self):
        if self.number == None:
            return None
        else:
            return ['%d%s' % (self.number, self.abbrevMap[i]) for i in self.missingColors]

class PartialGroup(Group):
    def addTile(self, tile):
        if type(tile) == str:
            self.__add_single_tile__(tile)
        elif type(tile) in (list, tuple):

            for t in tile:
                self.__add_single_tile__(t)
        else:
            raise TypeError("must provide addTile with string or list")
