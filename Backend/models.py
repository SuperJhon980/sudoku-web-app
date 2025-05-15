# models.py is to handle data validation from the frontend api requests
from pydantic import BaseModel
from typing import List

# Define the shape of the expected request data
class Cell(BaseModel):
    value: int | None
    isEditable: bool
    isValid: bool

class BoardData(BaseModel):
    board: List[List[Cell]]  # 9x9 Sudoku board


class MoveData(BaseModel):
    board: List[List[Cell]] # 9x9 sudoku board
    row: int
    column: int