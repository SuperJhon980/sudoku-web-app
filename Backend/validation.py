# validation logic
# ---------------
# Each validation function validates through checking the set of numbers
# is equal to 9. I don't use magic numbers but then I use incorrect lengths that are also 9
# that don't match the actual set I am checking. i.e. square validation
# I should have a constant of setLength or something. But whatever, i'm learning
#
# Also, zero count is included in validation because internal board representation has
# empty cells as zeros. By adding zero count, we are adding empty cells to the set length
# ---------------

# controller function for checking solution
# mustn't have any zeros in it. I know it could be faster but idc. I am learning and I 
# want to focus on other features that are more important
def checkBoardSolution(board):
    zeroCount = 0
    for row in board:
        zeroCount += row.count(0)
    return (boardValidation(board) and zeroCount == 0)

# controller function for board validation
def boardValidation(board):
    return ( validateRows(board) and
        validateColumns(board) and 
        validateSquares(board)
    )
    
# validate rows
def validateRows(board):
    isValid = True
    for row in board:
        nums = [n for n in row if n != 0]
        zeroCount = row.count(0)
        isValid = isValid and (len(row) == (len(set(nums)) + zeroCount))
    return isValid

# validate columns
def validateColumns(board):
    isValid = True
    for column in range(len(board)):
        nums = []
        zeroCount = 0
        for row in range(len(board)):
            if(board[row][column] != 0):
                nums.append(board[row][column])
            else:
                zeroCount += 1
        isValid = isValid and (zeroCount + len(set(nums))) == len(board)
    return isValid

# validate squares
def validateSquares(board):
    isValid = True
    for squareRow in range(3):      #Get the square row and column
        for squareColumn in range(3):
            nums = []
            zeroCount = 0       
            for innerRow in range(3):
                for innerColumn in range(3):
                    row = squareRow * 3 + innerRow          #Get the row and column of the cells within the square
                    column = squareColumn * 3 + innerColumn
                    if(board[row][column] != 0):
                        nums.append(board[row][column])
                    else:
                        zeroCount += 1          #Internal board state sets empty cells to zero
            isValid = isValid and (len(set(nums)) + zeroCount) == len(board)        #Check that the set of numbers (unique) is == to 9 (len of board)
    return isValid

# Controller function for move validation
def moveValidation(board, row, column):
    num = board[row][column]
    return (validateRow(board, row, num) and
            validateColumn(board, column, num) and
            validateSquare(board, row, column, num))

def validateRow(board, row, num):
    return board[row].count(num) == 1

def validateColumn(board, column, num):
    count = 0
    for row in range(len(board)):
        if board[row][column] == num:
            count += 1
    return count == 1

def validateSquare(board, numRow, numColumn, num):
    squareRow = (numRow // 3) * 3
    squareColumn = (numColumn // 3) * 3
    count = 0
    for row in range(3):
        for column in range(3):
            if board[squareRow + row][squareColumn + column] == num:
                count += 1
    return count == 1
