#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import copy
import time
import difflib

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


#def checkConstraints(board)
def checkComplete(board):
    #check that the size of all values in dict is 0
    for i in board.values():
        if i==0:
            return False
    #print("Complete")
    return True
    

def posVals(board): #remove illegal values from positions in d
    #print("getting posVals for")
    #print_board(board)
    d= {}
    for k in board.keys():
        if board[k]==0:
            d[k]= [1,2,3,4,5,6,7,8,9]
    squares= [['A1','A2','A3','B1','B2','B3','C1','C2','C3'],['A4','A5','A6','B4','B5','B6','C4','C5','C6'],['A7','A8','A9','B7','B8','B9','C7','C8','C9'],
        ['D1','D2','D3','E1','E2','E3','F1','F2','F3'],['D4','D5','D6','E4','E5','E6','F4','F5','F6'],['D7','D8','D9','E7','E8','E9','F7','F8','F9'],
        ['G1','G2','G3','H1','H2','H3','I1','I2','I3'],['G4','G5','G6','H4','H5','H6','I4','I5','I6'],['G7','G8','G9','H7','H8','H9','I7','I8','I9']]
    for key in d.keys():
        a= [k for k in board.keys() if key[0] in k and k !=key] #row
        b= [k for k in board.keys() if key[1] in k and k !=key] #col
        c= []
        for k in squares:
            if key in k:
                for i in k:
                    if i !=key:
                        c.append(i)
        illegal= a+b+c
        badVals = set()
        for i in illegal:
            if board[i]!=0:
                badVals.add(board[i])
        for val in badVals:
            if val in d[key]:
                d[key].remove(val)
        #print(key, ": ", d[key])     
        if len(d[key])==0:
            #print(key, " has no possible values")
            return None
    
    return d

def backtracking(board):

    """Takes a board and returns solved board."""
    # TODO: implement this
    d = {} #pos to possible values
    #print_board(board)
    #print("backtrack")
    return backtrack(board)

def backtrack(board):
    print_board(board)
    #print("in backtrack call")
    #1. check termination of recursion: no 0s in the board
    #print("current board: ")
    #print_board(board)
    if checkComplete(board): 
        return board

    #2. select unassigned variable using min remaining val heuristic (least amt of possible vals)
    min_len = 10
    d= posVals(board)
    for k in d.keys():
        if len(d[k])<min_len:
            min_len = len(d[k])
            minL = k
    #k is nextval
    #print("min Val: ", minL, ": ", d[minL])
    vals= d[minL]
    d.pop(minL)
    domains= copy.deepcopy(d)
    for i in vals:
        #print("in for loop")
    #3. for each val in possible vals (heuristic choose):
    #   if val is consistent with assignment:
        board[minL]=i
        # add {var = val} to assignment
        #print("attempting ", minL, " = ", i)
        d= posVals(board)
        #forward check
        if d is not None:
            result=  backtrack(board)
         #   print("CHECK BEFORE")
         #   print_board(board)
            if result is not None: return result
        #print(i, "in ", minL, "didnt work. Next")
        d= domains
        board[minL]= 0
        
        #remove {var = val} from assignment -- assignment does not work
    #print("returning none")
    return None


if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        print("Solution:")
        print_board(solved_board)
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        times= []
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)
            start = time.time()
            # Solve with backtracking
            solved_board = backtracking(board)
            end = time.time()
            times.append(end-start)
            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")