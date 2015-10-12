__author__ = 'johnthompson'

from searchPrimitives import findPlays

def bestOpeningPlay( rack ):
    return biggestPlay(rack, [])

def biggestPlay( rack, existingGroups):
    tableTiles = []
    for group in existingGroups:
        tableTiles += group.getTiles()

    groupings, remaining = findPlays(rack+tableTiles, None, tableTiles)
    used = list( set(rack) - set(remaining))
    return groupings, remaining, used