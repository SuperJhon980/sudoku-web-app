# This file contains the sudoku puzzle generator logic
from validation import boardValidation, checkBoardSolution, moveValidation
import random

# The logic to create the new sudoku puzzle
# First create the solution
def createNewSudokuPuzzle():
    board = [[0 for _ in range(9)] for _ in range(9)]
    board = createSolution(board)
    return board

# This function creates the solution to the puzzle through randomizers
# and checking validity at each number
def createSolution(board):
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


board = createNewSudokuPuzzle()

for row in board:
    print(row)

print("The board is valid: " + str(boardValidation(board)))
print("The board is solved: " + str(checkBoardSolution(board)))