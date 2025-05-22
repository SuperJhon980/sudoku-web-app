# This file contains the sudoku puzzle generator logic
from validation import boardValidation, checkBoardSolution, moveValidation
import random
import heapq

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

    def removeSolution(self, num):
        if not self.hasSolution and num in self.solutionSet:
            self.solutionSet.remove(num)
    
    def addSolution(self, num):
        self.solutionSet.append(num)

    def getCount(self):
        return len(self.solutionSet)
    
    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        if value == 0:
            self.hasSolution = False
            self.solutionSet = [n + 1 for n in range(9)]
        else:
            self.hasSolution = True
            self.solutionSet = [self.number]
        print(f"Cell at {self.row}, {self.col} hasSolution: {self.hasSolution}")
        print(f"Solution is {self.number}")

# This is the sudokuBoard object
# 9x9 grid with each element a sudoku CELL
# Keeps track of zeroCount to keep track later if there are any emptyCells
class SudokuBoard:
    def __init__(self):
        self.board = [[SudokuCell(0, y, x) for x in range(9)] for y in range(9)]
        self.zeroCount = 81
        self.heap = []
        self.buildHeap()

    def buildHeap(self):
        self.heap = []
        for row in self.board:
            for cell in row:
                if not cell.hasSolution:
                    heapq.heappush(self.heap, (cell.getCount(), cell.row, cell.col))

    def updateSolutionSets(self, solvedCell):
        neighbors = getNeighbors(solvedCell.row, solvedCell.col)
        for coords in neighbors:
            cell = self.board[coords[0]][coords[1]]
            cell.removeSolution(solvedCell.number)
        self.buildHeap()

    def pickNewCell(self):
        coords = heapq.heappop(self.heap)
        cell = self.board[coords[1]][coords[2]]
        return cell

    def print(self):
        for row in self.board:
            newRow = []
            for cell in row:
                newRow.append(cell.number)
            print(newRow)

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
    board = createSolution(board)
    return board


def createSolution(board):
    while board.zeroCount > 0:
        
        cell = board.pickNewCell()
        failsafe = 0
        pickNewSolution(board, cell, failsafe)
        board.updateSolutionSets(cell)
        board.zeroCount -= 1
        board.print()
    return board

def pickNewSolution(board, cell, failsafe):
    cell.number = random.choice(cell.solutionSet)
    while(not moveValidation(board.getBoard(), cell.row, cell.col)):        # Check that the random number doesn't invalidate the solution
        print(cell.solutionSet)
        cell.number = random.choice(cell.solutionSet)
        print(cell.number)
        if failsafe > 2:
            return board
        failsafe += 1


board = createNewSudokuPuzzle()
# board = SudokuBoard()
neighbors = getNeighbors(1, 5)
for x in neighbors:
    cell = board.board[x[0]][x[1]]
    # cell.number = 1

board.print()
newBoard = board.getBoard()
print()
print("The board is valid: " + str(boardValidation(newBoard)))
print("The board is solved: " + str(checkBoardSolution(newBoard)))
board.print()















# Here is the graveyard. Functions that didn't work

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