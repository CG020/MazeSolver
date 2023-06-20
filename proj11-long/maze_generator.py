#! /usr/bin/python3

import sys
import random



def build_grid(wid,hei):
    retval = []
    for x in range(wid):
        this_col = []
        for y in range(hei):
            this_col.append( [0, {(x,y)} ] )
        retval.append(this_col)
    return retval



def build_links(grid, wid,hei):
    # this is a list of all of the possible edges in the map.  It's a quite
    # gigantic, one-dimensional array
    possible_edges = []
    for x1 in range(0,wid-1):
        x2 = x1+1
        for y in range(0,hei):
            possible_edges.append( (x1,y,x2,y) )     # horizontal links
    for x in range(0,wid):
        for y1 in range(0,hei-1):
            y2 = y1+1
            possible_edges.append( (x,y1,x,y2) )     # vertical links


    # mix up the list of all possible links; this will be our sequence in which
    # we will attempt to link nodes together.  We don't know how many of these
    # links we'll use, because we'll have to skip over some (as they would
    # create cycles)
    random.shuffle(possible_edges)

    # How do we know that we've linked everything together?  When location (0,0)
    # in the grid is linked to every other node, we're done.

    i = 0
    while len(grid[0][0][1]) < wid*hei:
        (x1,y1,x2,y2) = possible_edges[i]
        i += 1

        # is this a vertical or horizontal link?  Sanity-check that it's not
        # already in place
        if x1 != x2:
            assert x2 == x1+1
            assert y2 == y1
            assert (grid[x1][y1][0] & 8) == 0
            assert (grid[x2][y2][0] & 4) == 0
        else:
            assert x2 == x1
            assert y2 == y1+1
            assert (grid[x1][y1][0] & 2) == 0
            assert (grid[x2][y2][0] & 1) == 0

        set1 = grid[x1][y1][1]
        set2 = grid[x2][y2][1]
        assert (x1,y1) in set1
        assert (x2,y2) in set2

        if set1 is set2:
            continue      # can't use this link!

        if x1 != x2:
            grid[x1][y1][0] |= 8
            grid[x2][y2][0] |= 4
        else:
            grid[x1][y1][0] |= 2
            grid[x2][y2][0] |= 1

        # add all of the members from set2 into set1
        set1.update(set2)

        # then, update all of the grid entries, for set2, to point to set1
        for x,y in set2:
            grid[x][y][1] = set1



def print_grid(grid, wid,hei):
    start = ( random.randint(0,wid-1), random.randint(0,hei-1) )

    end = start
    while end == start:
        end = ( random.randint(0,wid-1), random.randint(0,hei-1) )


    for y in range(hei):
        # this is the "room" line...
        for x in range(wid-1):
            if (x,y) == start:
                print("S", end='')
            elif (x,y) == end:
                print("E", end='')
            else:
                print("#", end='')

            if grid[x][y][0] & 8:
                print("#", end='')
            else:
                print(" ", end='')

        if   (wid-1,y) == start:
            print("S")
        elif (wid-1,y) == end:
            print("E")
        else:
            print("#")

        # this is the 'vertical edges' line.  Skip it if we're on the bottom edge
        if y == hei-1:
            break

        for x in range(wid-1):
            if grid[x][y][0] & 2:
                print("# ", end="")
            else:
                print("  ", end="")
        if grid[wid-1][y][0] & 2:
            print("#")
        else:
            print(" ")



def main(wid, hei):

    # every entry in the grid has two components: an integer, representing bit
    # flags: 1-up, 2-down, 4-left, 8-right; and a reference to a set, which
    # contains all of the (x,y) coordinates of all of the cells which are
    # connected to this cell.  When we begin, all such sets have only a single
    # node.
    grid = build_grid(wid,hei)

    # create all of the links 
    build_links(grid, wid,hei)

    print_grid(grid, wid,hei)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: Give the width and height of the maze, as command-line arguments!", file=sys.stderr)
        exit(1)
    main( int(sys.argv[1]), int(sys.argv[2]) )

