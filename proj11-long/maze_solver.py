'''
File: maze_solver.py
Author: Camila Grubb
Course: CSC 120
Purpose: This program is given a maze made out of text and solves the maze
by finding the path from the Start cell to the End cell. This program utilizes
a modified TreeNode class along with 'dump' functions that perform certain
actions involving the cells of the maze.
'''

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

    def add_child(self, node_val):
        '''
        Appends the value being passed to the method to the list within
        the node being called upon
        :param node_val: integer
        '''
        self.children.append(node_val)

    def is_leaf(self):
        '''
        Checks if the object being called upon is a leaf meaning it had
        no children
        '''
        if len(self.children) > 0:
            return False
        return True


def checks(s_count, e_count, cells2, start, end):
    '''
    This function checks all the necessary issues that may arise in an invalid
    maze text. It checks if there exists a Start, an End, if there is not more
    than one
    :param s_count: integer
    :param e_count: integer
    :param cells2: list of tuples
    :param start: a tuple
    :param end: a tuple
    :return: string or a tuple where file[0] is list if cells, file[1] if
    Start tuple and file[1] is End tuple
    '''
    try:
        assert s_count > 0 #  checks if there exists a Start
        assert e_count > 0 #  same with End
        try:
            assert s_count == 1 #  checks that there is only one Start
            try:
                assert e_count == 1 #  checks there is only one End
                return sorted(cells2), start, end #  if checks passed, returns
                #  file info
            except AssertionError:
                print("ERROR: The map has more than one END position")
                return "Error"
        except AssertionError:
            print("ERROR: The map has more than one START position")
            return "Error"
    except AssertionError:
        print(
            "ERROR: Every map needs exactly one START and exactly one END "
            "position")
        return "Error"


def read_file(file):
    '''
    This function reads the input file.
    :param file: txt file
    :return: string or a tuple where file[0] is list if cells, file[1] if
    Start tuple and file[1] is End tuple
    '''
    maze_file = open(file, "r").readlines()
    cells, cells2, s_count, e_count, start, end = [], [], 0, 0, None, None
    for item in maze_file:
        cells.append(list(item))
    for index in range(len(cells)): #  iterates through each character
        for x in range(len(cells[index])):
            try:
                #  checks for valid characters
                assert cells[index][x] in ('#', 'S', "E", " ", "\n")
                if cells[index][x] == "#": #  appends valid characters
                    cells2.append((x, index))
                elif cells[index][x] == "S":
                    s_count += 1 #  keeps track of how many Starts exist
                    cells2.append((x, index))
                    start = (x, index) #  sets the Start position
                elif cells[index][x] == "E":
                    e_count += 1 #  keeps track of how many Ends exist
                    cells2.append((x, index))
                    end = (x, index) #  sets the End position
            except AssertionError:
                print("ERROR: Invalid character in the map")
                return ("Error")
    return checks(s_count, e_count, cells2, start, end)


def dump_cells(file):
    '''
    This function prints all the cells in the file with marks on the
    Start and End
    :param file: a tuple where file[0] is list if cells, file[1] if Start tuple
    and file[1] is End tuple
    '''
    print("DUMPING OUT ALL CELLS FROM THE MAZE:")
    for item in file[0]:
        if item == file[1]: #  checks if current cell is equal to Start tuple
            print("  " + str(item) + "    START")
        elif item == file[2]: #  checks if current cell is equal to End tuple
            print("  " + str(item) + "    END")
        else:
            print("  " + str(item))


def child(root, dir1, dir2,child, node_list):
    '''
    This function adds the cell being checked to the current node child list.
    It removes the cell from the node_list so repetition does not occur.
    It then recurses through that newly create child, if the recursive
    statement returns None, the function returns the root. If not, it will
    sets the child to its correct value.
    :param root: a Tree node
    :param dir1: an integer
    :param dir2: an integer
    :param child: the current index in the list if a node (integer)
    :param node_list: a list of tuples
    :return: a tree
    '''
    root.add_child(TreeNode((dir1, dir2))) #  appends value to child
    node_list.remove((dir1, dir2))
    place = dump_tree(root.children[child], node_list)
    if place is None:
        return root
    else:
        root.children[child] = place


def dump_tree(root, node_list):
    '''
    This function creates a tree from the cells in the maze text.
    :param root: a tree node
    :param node_list: list of tuples
    :return: a tree
    '''
    if root is None:
        return None
    #  check  if position above current cell exists in list if cells in text
    if (root.val[0], root.val[1] - 1) in node_list:
        #  if exists, creates the child utilizing child function
        child(root,root.val[0], root.val[1] - 1,0, node_list)
    else:
        root.add_child(None) #  if doesnt exist, appends None to current child
    if (root.val[0], root.val[1] + 1) in node_list: # checks below position
        child(root,root.val[0], root.val[1] + 1, 1, node_list)
    else:
        root.add_child(None) #  if doesnt exist, appends None to current child
    if (root.val[0] - 1, root.val[1]) in node_list: #  checks left position
        child(root, root.val[0] - 1, root.val[1], 2, node_list)
    else:
        root.add_child(None) #  if doesnt exist, appends None to current child
    if (root.val[0] + 1, root.val[1]) in node_list: #  checks right position
        child(root,root.val[0] + 1, root.val[1], 3, node_list)
    else:
        root.add_child(None) #  if doesnt exist, appends None to current child
    return root


def print_dump_tree(root, indent=" "):
    '''
    This function prints the cells of a maze in the format of its tree.
    :param root: a tree
    :param indent: a string
    '''
    print(indent,root.val)
    for child in root.children: #  iterates through the tree
        if child is not None:
            print_dump_tree(child,indent+" |") #  recursively prints the
            #  children of the nodes iterating through tree adding | as indents


def dump_solution(root, end):
    '''
    This function returns the correct path through the maze that lists the
    cells that lead from Start to End
    :param root: a tree
    :param end: a tuple
    :return: a list of tuples
    '''
    if root is None:
        return None
    if root.val == end: #  checks if reached the End
        return []
    elif root.is_leaf(): #  if the root has no children None gets recursion out
        return None
    for child in root.children: #  iterates through children of current root
        path = dump_solution(child, end)
        if path is not None: #  adds the path that reaches the end recursively
            return [child.val] + path


def dump_size(file):
    '''
    This function prints the height and width of the maze.
    :param file: a list of tuples
    '''
    print("MAP SIZE:")
    height = []
    width = []
    for item in file: #  stores the y values in a list 'height'
        height.append(item[1])
    for item in file: #  stores the x values in a list 'width'
        width.append(item[0])
    print(f"  wid: {max(width)+1}") #  prints the max width
    print(f"  hei: {max(height)+1}") #  prints the max height


def print_solved_maze(path, file):
    '''
    This function prints the maze with the correct path that represents a
    solved maze replaced with '.' characters
    :param path: a list of tuples
    :param file: a text file (the maze)
    '''
    print("SOLUTION:")
    path.pop(-1) #  removes End cell
    maze_file = open(file, "r").readlines()
    for x in range(len(maze_file)): #  iterates through every character in maze
        for y in range(len(maze_file[x])):
            if (y,x) in path: #  if current cell is in the correct path list
                print(".", end="") #  replaces that character with '.'
            else: #  otherwise prints the character in the maze
                print(maze_file[x][y], end="")


def main():
    try: #  checks that the input file is valid
        input_file = input()
        file = read_file(input_file) #  reads file to get cells, Start, and End
        root = TreeNode(file[1]) #  sets root node as Start
        if file == "Error": #  file checks validity so if returns Error,
            return #  terminate sthe program
        try:
            command = input()
            assert command in ("dumpCells", "dumpTree", "dumpSolution",
                        "dumpSize", "") #  checks that the command is valid
            if command == "dumpCells":
                dump_cells(file)
                return
            elif command == "dumpTree":
                print("DUMPING OUT THE TREE THAT REPRESENTS THE MAZE:")
                file[0].remove(file[1]) #  must remove Start cell
                tree = dump_tree(root, file[0]) #  makes tree
                print_dump_tree(tree) #  prints the tree
            elif command == "dumpSolution":
                print("PATH OF THE SOLUTION:")
                file[0].remove(file[1]) #  must remove Start cell
                tree = dump_tree(root, file[0]) #  makes tree
                path = dump_solution(tree, file[2]) #  makes correct path list
                print(f"  {file[1]}")
                for item in path: #  prints the cells in correct path
                    print(f"  {item}")
            elif command == "dumpSize":
                dump_size(file[0])
            else:
                file[0].remove(file[1]) #  must remove Start cell
                tree = dump_tree(root, file[0]) #  makes tree
                path = dump_solution(tree, file[2]) #  finds correct path
                print_solved_maze(path, input_file) #  prints solved maze
        except AssertionError:
            print(f"ERROR: Unrecognized command {command}")
    except FileNotFoundError:
        print(f"ERROR: Could not open file: {input_file}")


if __name__ == "__main__":
    main()