# This file contains the sudoku puzzle generator logic
from validation import boardValidation, checkBoardSolution, moveValidation
import random
import heapq
import copy
import queue
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

    # Takes away a number from the solutionSet. Used in constraint propogation
    def removeSolution(self, num):
        if not self.hasSolution and num in self.solutionSet:
            self.solutionSet.remove(num)
    
    # Adds a number from the solutionSet. Used in backtracking
    def addSolution(self, num):
        if not self.hasSolution and num not in self.solutionSet:
            self.solutionSet.append(num)

    # Gets the count. Used for minHeap to pick most constrained variable
    def getCount(self):
        return len(self.solutionSet)
    
    @property
    def number(self):
        return self._number

    # Sets the number and updates hasSolution and solutionSet
    # Partly incorrect because setting it to zero does not mean that
    # numbers 1-9 are in solutionSet
    @number.setter
    def number(self, value):
        self._number = value
        if value == 0:
            self.hasSolution = False
            self.solutionSet = [n + 1 for n in range(9)] # This is not true... Corrected in updateSolutionSets of the board object
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
        self.digitCount = {i: 0 for i in range(10)}
        self.digitCount[0] = 81
        self.heap = []  # minHeap to pick most constrained cell to fill (forward checking)
        self.buildHeap()
        self.diffStack = []
        self.solution = []

    # Builds the minHeap from all the cells
    def buildHeap(self):
        self.heap = []
        for row in self.board:
            for cell in row:
                if not cell.hasSolution:
                    # minHeap ordered by len(solutionSet), row, col
                    heapq.heappush(self.heap, (cell.getCount(), cell.row, cell.col))

    # Checks if the board hasSolution
    def hasNoZeros(self):
        return self.digitCount[0] == 0

    # Wrapper function that manages all internals of sudoku Board when we want to
    # change a cell's number. This includes diffStack, constraint propogation, and
    # zeroCount
    def setCell(self, row, col, num):
        cell = self.board[row][col]
        self.stackDiff(cell)
        numIsZero = num == 0
        if numIsZero:
            self.digitCount[0] += 1
            self.digitCount[cell.number] -= 1
        else:
            self.digitCount[0] -= 1
            self.digitCount[num] += 1
        cell.number = num
        self.updateSolutionSets(row, col, numIsZero)
        
    # This function returns True if by removing the given cell it would create a symmetric
    # sudoku puzzle that has removed all the numbers for two given numbers
    def cellMakesSymmetry(self, cell):
        numZeroDigits = 0
        for n in range(9):
            if self.digitCount[n + 1] == 0:
                numZeroDigits += 1

        if self.digitCount[cell.number] == 1:
            numZeroDigits += 1
        return numZeroDigits > 1
    

    # This is to snip off solutionCount early if we have similar number
    # Function returns true if the boards current solution is the same
    # as the created solution
    def isChildToSolution(self):
        board = self.getBoard()
        for row in range(9):
            for col in range(9):
                puzzleNum = board[row][col]
                solutionNum = self.solution[row][col]
                if puzzleNum != 0 and puzzleNum != solutionNum:
                    return False
        return True

    # This function puts a move on the diffStack
    # Adds a move to the history
    def stackDiff(self, cell):
        newDiff = Diff(cell)
        self.diffStack.append(newDiff)

    # Function updates solutionsets after a cell's number has been updated
    # This is the constraint Propagation algorithm for finding solutions. Goated frfr
    def updateSolutionSets(self, row, col, numIsZero):
        # getNeighbors gets all the neighbors
        neighbors = getNeighbors(row, col)
        updatedCell = self.board[row][col]
        for coords in neighbors:
            cell = self.board[coords[0]][coords[1]]
            if(numIsZero): 
                cell.addSolution(self.diffStack[-1].number)
                updatedCell.removeSolution(cell.number)
            else:
                cell.removeSolution(updatedCell.number)

    def setSolution(self, solution):
        print(f"Solution is valid: {checkBoardSolution(solution)}")
        print("Solution shown below")
        self.print()
        print("---------------------------")
        self.solution = solution

    # Undo move from diffStack
    # Goes a step back on the diffStack. 
    def undoMove(self):
        diff = self.diffStack.pop()
        self.setCell(diff.row, diff.col, diff.number)
        # setCell stacks a diff but we don't want to do that because
        # we don't want to track the undo move that we just did
        # so we pop that move off stack
        self.diffStack.pop() 

    
    # Pops a cell from minHeap (most constrained cell)
    def pickNewCell(self):
        self.buildHeap()
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
        self.number = cell.number
        self.row = cell.row
        self.col = cell.col
    
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
    if not board.hasNoZeros():
        cell = board.pickNewCell()
        if cell.solutionSet: # Cell has possible solutions, move forward
            trySolution(board, cell, random.choice(tuple(cell.solutionSet)))
            # ✅ Don’t reset fails immediately
            return createSolution(board, fails)
        else: # No solution found
            for _ in range(fails): # Must backtrack
                board.undoMove()
            return createSolution(board, fails + 1)
    print()
    return board  # Success: all zeros filled

# This function tries a given solution and returns true if that solution was valid
def trySolution(board, cell, num):
    board.setCell(cell.row, cell.col, num)
    if moveValidation(board.getBoard(), cell.row, cell.col):
        return True  # Found a valid move
    return False  # Exhausted all possibilities, no valid number found
    
    
# This is controller function that calls remove hints until hintCounter is reached
def createPuzzle(board):
    hintCounter = 81 - 57
    cellQueue = buildRandomQueue(board)
    while(cellQueue.qsize() > hintCounter):
        removeHints(board, cellQueue.get(), cellQueue)
        print(f"Hints removed: {81 - cellQueue.qsize()}")
    return board

# removeHints gets the next cell in the shuffled queue and
# removes the number in the cell and checks that there is still a unique answer
# It backtracks if there is not a unique solution to the board
def removeHints(board, cell, cellQueue):
    if board.cellMakesSymmetry(cell):
        print("****Tried again because of symmetry****")
        return
    else:
        board.setCell(cell.row, cell.col, 0)
    
    if not hasUniqueSolution(board):
        board.undoMove()
        cellQueue.put(cell) # Send the cell to the back of the queue
        return
    print("Removed another hint")
    board.print()
    return

# This function acts as a controller that initiates a recursive solution-counting process
# and interprets the result to determine solution uniqueness.
def hasUniqueSolution(board):
    countHolder = [0]   # imutable object counter for recursive call
    countSolutions(board, countHolder)
    if countHolder[0] == 1:
        return True
    elif countHolder[0] > 1:
        return False
    else:
        assert False, "Somehow found no solutions to a solvable board"

# This function counts the number of solutions of a given unsolved Sudoku Board using Depth First Search
# countHolder is a mutable object to have a maxSolution search (2 in my case for uniqueness)
def countSolutions(board, solutionCount):
    # Base case: board is solved
    if board.hasNoZeros() and checkBoardSolution(board.getBoard()):
        print(f"Found solution #{solutionCount[0] + 1}")
        print(f"Solution isChild: {board.isChildToSolution()}")
        #board.print()
        if not board.isChildToSolution():
            solutionCount[0] += 2
        else:
            solutionCount[0] += 1 # Increment solutionCount
        return 
    
    # Solution cap
    if solutionCount[0] > 1:
        return

    cell = board.pickNewCell()
    if not cell.solutionSet:
        return   # Hit a dead end where cell has no possible options
    
    # We will try every possible solution as these are different branches in DFS tree
    for digit in cell.solutionSet:
        if trySolution(board, cell, digit): # Returns true if digit was valid
            countSolutions(board, solutionCount)    # Let's go one step deeper into tree
        board.undoMove()    # Make sure to backtrack to explore rest of the tree
    return
    




# Helper function that creates a shuffled queue of the cells in the sudoku Board
# This is to randomly pick numbers to remove
def buildRandomQueue(board):
    q = queue.Queue()
    cells = [cell for row in board.board for cell in row]
    random.shuffle(cells)
    for cell in cells:
        q.put(cell)
    return q

# The logic to create the new sudoku puzzle
# First create the solution
def createNewSudokuPuzzle():
    board = SudokuBoard()
    board = createSolution(board, 0)
    board.setSolution(board.getBoard())
    board = createPuzzle(board)
    return board


board = createNewSudokuPuzzle()
#board = SudokuBoard()
#board = createSolution(board, 0)

newBoard = board.getBoard()
print("-------Final Output--------")
board.print()
print("---------")
print("The board is valid: " + str(boardValidation(newBoard)))
print("The board is solved: " + str(checkBoardSolution(newBoard)))
print("---------")

