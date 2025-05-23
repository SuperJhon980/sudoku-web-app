# This file contains the sudoku puzzle generator logic
from validation import boardValidation, checkBoardSolution, moveValidation
import random
import heapq
import copy
# SudokuCell class. It has it's own coords and number
# Also holds a solution set that is used during puzzle generation
class SudokuCell:
    def __init__(self, number, row, col):
        self.row = row
        self.col = col
        self.solutionSet = [n + 1 for n in range(9)]

        if number in self.solutionSet:
            self.number = number
            self.solutionSet = [number]  # only possible solution is the assigned number
            self.hasSolution = True
        else:
            self.number = 0  # no number assigned
            self.hasSolution = False

    # Takes away a number form the solutionSet
    def removeSolution(self, num):
        if not self.hasSolution and num in self.solutionSet:
            self.solutionSet.remove(num)
    
    # Adds a number from the solutionSet. Used in retracing
    def addSolution(self, num):
        self.solutionSet.append(num)

    # Gets the count. Used for minHeap to pick most constrained variable
    def getCount(self):
        return len(self.solutionSet)
    
    @property
    def number(self):
        return self._number

    # Sets the number and updates hasSolution
    @number.setter
    def number(self, value):
        self._number = value
        if value == 0:
            self.hasSolution = False
            self.solutionSet = [n + 1 for n in range(9)]
        else:
            self.hasSolution = True
            self.solutionSet = [self.number]
        # print(f"Cell at {self.row}, {self.col} hasSolution: {self.hasSolution}") # Troubleshooting
        # print(f"Solution is {self.number}")

# This is the sudokuBoard object
# 9x9 grid with each element a sudoku CELL
# Keeps track of zeroCount to keep track later if there are any emptyCells
class SudokuBoard:
    def __init__(self):
        self.board = [[SudokuCell(0, row, col) for col in range(9)] for row in range(9)]
        self.zeroCount = 81
        self.heap = []  # minHeap to pick most constrained cell to fill (forward checking)
        self.buildHeap()
        self.diffStack = []

    # Builds the minHeap from all the cells
    def buildHeap(self):
        self.heap = []
        for row in self.board:
            for cell in row:
                if not cell.hasSolution:
                    # minHeap ordered by len(solutionSet), row, col
                    heapq.heappush(self.heap, (cell.getCount(), cell.row, cell.col))

    # Function updates solutionsets after a cell's solution has been picked
    def updateSolutionSets(self, solvedCell, diff):
        # getNeighbors gets all the neighbors
        neighbors = getNeighbors(solvedCell.row, solvedCell.col)
        for coords in neighbors:
            cell = self.board[coords[0]][coords[1]]
            diff.addPrunedNeighbor(cell)    # Adds history of neighbors for backtracking
            cell.removeSolution(solvedCell.number)
        self.buildHeap()

    # Undo move from diffStack
    def undoMove(self):
        diff = self.diffStack.pop()
        oldCell = diff.assignedCell
        self.board[oldCell.row][oldCell.col] = oldCell
        for neighbor in diff.prunedNeighbors:
            self.board[neighbor.row][neighbor.col] = neighbor
    
    # Pops a cell from minHeap
    def pickNewCell(self):
        coords = heapq.heappop(self.heap)
        cell = self.board[coords[1]][coords[2]]
        return cell

    # Just to see the sudoku puzzle during production
    def print(self):
        for row in self.board:
            newRow = []
            for cell in row:
                newRow.append(cell.number)
            print(newRow)

    # Getting a 2d list of just the numbers to match validation logic I wrote before
    # writing all of this
    def getBoard(self):
        board = []
        for row in self.board:
            newRow = []
            for cell in row:
                newRow.append(cell.number)
            board.append(newRow)
        return board
    
    def getCell(self, row, col):
        return self.board[row][col]

class Diff:
    def __init__(self, cell):
        self.assignedCell = copy.deepcopy(cell)
        self.prunedNeighbors = []

    def addPrunedNeighbor(self, cell):
        self.prunedNeighbors.append(copy.deepcopy(cell))
    
# Helper function that returns a list of tuples of all neighbors of a given cell
def getNeighbors(row, col):
    squareRow = (row // 3) * 3
    squareCol = (col // 3) * 3
    neighbors = []
    for x in range(3):
        for y in range(3):
            neighbors.append((row, (x * 3) + y))
            neighbors.append(((x * 3) + y, col))
            neighbors.append((squareRow + x, squareCol + y))
    neighbors = set(neighbors)
    neighbors.remove((row, col))
    return neighbors


# The logic to create the new sudoku puzzle
# First create the solution
def createNewSudokuPuzzle():
    board = SudokuBoard()
    board = createSolution(board, 0)
    return board

# Known refactoring possibility that I didn't want to spend more time thinking about:
# Reset fails to zero after making it past a certain dead end...
# I still can't tell if it does reset to zero or not. ChatGPT brainwashed me into thinking it did...
#
# Here is how this works:
# Recursion until the board is filled (no zero's)
# The board does forward checking to pick a value for the sudoku cell that is now most constrained by
# it's neighbors. If a cell is found that now has no more options to pick from, we backtrack once more than
# we did last time (starting from 0). 
#
# Here is the refactoring opportunity. If a deadend happens that takes 3 undos, and then there is a
# future, independent, dead end that only takes one undo, well it's gonna do 4 now instead of just the one
# Figure out a way to reset the number of undos to zero once you've made it past a given dead end
#
# Good luck
def createSolution(board, fails):
    if board.zeroCount != 0:
        cell = board.pickNewCell()
        newDiff = Diff(cell)    # Keep history of board for backtracking
        if pickNewSolution(board, cell): # Successfully found a solution, move forward
            board.updateSolutionSets(cell, newDiff) # Pass the diff in to keep history
            board.diffStack.append(newDiff) # diffStack is the history of the board
            board.zeroCount -= 1

            # ✅ Don’t reset fails immediately
            return createSolution(board, fails)
        else: # No solution found
            for _ in range(fails):
                board.undoMove()
                board.zeroCount += 1
            return createSolution(board, fails + 1)

    return board  # Success: all zeros filled

# This function picks a solution and returns a solution
# The cell chosen was forward checked already
# Returns false if we have hit a dead end
def pickNewSolution(board, cell):
    if not cell.solutionSet:
        return False  # No possible values, trigger backtracking
    cell.number = random.choice(tuple(cell.solutionSet))
    if moveValidation(board.getBoard(), cell.row, cell.col):
        return True  # Found a valid move
    else: # This else statement is chatGPT BLOAT. Lmao. What a waste...
        cell.solutionSet.remove(cell.number)  # Remove invalid choice and try again
        print("Shouldn't be here to my knowledge. Explore why you are")
        print("You'll learn something")
        print("ERROR ERROR ERROR REDACTED REDATCED REDACTED")

    return False  # Exhausted all possibilities, no valid number found
    


board = createNewSudokuPuzzle()
# board = SudokuBoard()


newBoard = board.getBoard()
print("---------")
board.print()
print("---------")
print("The board is valid: " + str(boardValidation(newBoard)))
print("The board is solved: " + str(checkBoardSolution(newBoard)))
print("---------")
















# Here is the graveyard. Functions that didn't work

# This didn't work because I need to have backtracking. Recursion works better
def graveyardCreateSolution(board):
    while board.zeroCount > 0:
        
        cell = board.pickNewCell()
        failsafe = 0
        pickNewSolution(board, cell, failsafe)
        board.updateSolutionSets(cell)
        board.zeroCount -= 1
        board.print()
    return board

# This function creates the solution to the puzzle through randomizers
# and checking validity at each number
def graveyardCreateSolution(board):
    for row in range(9):
        for column in range(9):
            board[row][column] = random.randint(1, 9)   # Generate the random number in 1-9
            failsafeCount = 0
            while(not moveValidation(board, row, column)):        # Check that the random number doesn't invalidate the solution
                board[row][column] = random.randint(1,9)
                failsafeCount += 1
                if failsafeCount > 10000:
                    return board
    return board