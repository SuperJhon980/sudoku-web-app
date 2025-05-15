from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from validation import boardValidation, moveValidation
from models import BoardData, MoveData, Cell
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Or ["http://127.0.0.1:5500"] for more control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to validate the Sudoku board
@app.post("/check-board")
def validate_board(data: BoardData):
    board = data.board
    is_valid = boardValidation(board)
    
    return {"valid": is_valid}

# Endpoint to validate the Sudoku board
@app.post("/check-move")
def validate_move(data: MoveData):
    board = data.board
    row = data.row
    column = data.column
    is_valid = moveValidation(board, row, column)
    
    return {"valid": is_valid}

