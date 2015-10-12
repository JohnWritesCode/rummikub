__author__ = 'johnthompson'
import itertools
from playables import PartialGroup, PartialRun

def create_new_set(existing_sets, target_set, new_tile):
    out = []
    for s in existing_sets:
        if s == target_set:
            new_s = s.clone()
            new_s.addTile(new_tile)
            out.append(new_s)
        else:
            out.append(s)
    return out

def try_set(remaining_tiles, putative_set):
    out = []
    for pair in itertools.combinations(remaining_tiles, 2):
        if pair[0] in putative_set.validAdds():
            expanded_set = putative_set.clone()
            expanded_set.addTile(pair[0])
            if pair[1] in expanded_set.validAdds():
                out.append(pair)
        elif pair[1] in putative_set.validAdds():
            expanded_set = putative_set.clone()
            expanded_set.addTile(pair[1])
            if pair[0] in expanded_set.validAdds():
                out.append((pair[1],pair[0]))
    return out


def findPlays(rack, existing_sets = None, required_tiles = None):
    if existing_sets == None:
        existing_sets = []
    current_best_sets = existing_sets
    current_best_remaining = rack[:]
    if required_tiles == None or required_tiles == []:
        tiles_satisfied = True
    else:
        tiles_satisfied = False

    for tile in rack:

        remaining_tiles = rack[:]
        remaining_tiles.remove(tile)
        if required_tiles != None:
            remaining_required = required_tiles[:]
            if tile in remaining_required:
                remaining_required.remove(tile)
        else:
            remaining_required = None

        ## try adding to existing sets
        for tileSet in existing_sets:
            if tile in tileSet.validAdds():
                produced_sets, produced_remaining_tiles = findPlays(remaining_tiles, create_new_set(existing_sets, tileSet, tile), remaining_required)
                if produced_sets != None: #used all required tiles
                    if len(produced_remaining_tiles) == 0:
                        return produced_sets, produced_remaining_tiles
                    elif len(produced_remaining_tiles) < len(current_best_remaining):
                        current_best_sets = produced_sets
                        current_best_remaining = produced_remaining_tiles
                        tiles_satisfied = True ## we have found a solution that does satisfy

        ## try creating a new run
        putative_run = PartialRun(tile)
        for pair in try_set(remaining_tiles, putative_run):
            test_run = putative_run.clone()
            test_run.addTile(pair[0])
            test_run.addTile(pair[1])
            test_tiles = remaining_tiles[:]
            test_tiles.remove(pair[0])
            test_tiles.remove(pair[1])
            test_sets = existing_sets[:]
            test_sets.append(test_run)
            if remaining_required != None:
                test_required = remaining_required[:]
                if pair[0] in test_required:
                    test_required.remove(pair[0])
                if pair[1] in test_required:
                    test_required.remove(pair[1])
            else:
                test_required = None
            produced_sets, produced_remaining_tiles = findPlays(test_tiles, test_sets, test_required)

            if produced_sets != None: # we found a valid solution
                if len(produced_remaining_tiles) == 0:
                    return produced_sets, produced_remaining_tiles
                elif len(produced_remaining_tiles) < len(current_best_remaining):
                    current_best_sets = produced_sets
                    current_best_remaining = produced_remaining_tiles
                    tiles_satisfied = True ## we have found a solution that does satisfy


        ## try creating a new group
        putative_group = PartialGroup(tile)
        for pair in try_set(remaining_tiles, putative_group):
            test_group = putative_group.clone()
            test_group.addTile(pair[0])
            test_group.addTile(pair[1])
            test_tiles = remaining_tiles[:]
            test_tiles.remove(pair[0])
            test_tiles.remove(pair[1])
            test_sets = existing_sets[:]
            test_sets.append(test_group)
            if remaining_required != None:
                test_required = remaining_required[:]
                if pair[0] in test_required:
                    test_required.remove(pair[0])
                if pair[1] in test_required:
                    test_required.remove(pair[1])
            else:
                test_required = None

            produced_sets, produced_remaining_tiles = findPlays(test_tiles, test_sets, test_required)
            if produced_sets != None: ## we used all required tiles
                if len(produced_remaining_tiles) == 0:
                    return produced_sets, produced_remaining_tiles
                elif len(produced_remaining_tiles) < len(current_best_remaining):
                    current_best_sets = produced_sets
                    current_best_remaining = produced_remaining_tiles
                    tiles_satisfied = True ## we have found a solution that does satisfy

    if tiles_satisfied:
        return current_best_sets, current_best_remaining
    else:  ## this was not a successful path
        return None, None
