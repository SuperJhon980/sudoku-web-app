# validation logic
# ---------------
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
        isValid = isValid and (len(row) == len(set(nums)))
    return isValid

# validate columns
def validateColumns(board):
    isValid = True
    for column in range(len(board)):
        nums = []
        for row in range(len(board)):
            if board[row][column] != 0:
                nums.append(board[row][column])
        isValid = isValid and len(set(nums)) == len(board)
    return isValid

# validate squares
def validateSquares(board):
    isValid = True
    for squareRow in range(3):
        for squareColumn in range(3):
            nums = []
            for innerRow in range(3):
                for innerColumn in range(3):
                    row = squareRow * 3 + innerRow
                    column = squareColumn * 3 + innerColumn
                    if(board[row][column] != 0):
                        nums.append(board[row][column])
            isValid = isValid and len(set(nums)) == len(nums)
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
