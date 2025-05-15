import { setupEventListeners } from './events.js';



// This is the client-side board state
let board = Array(9).fill(null).map(() =>
    Array(9).fill(null).map(() => ({
      value: null,
      isEditable: true,
      isValid: true
    }))
  );

/* automate the creation of the sudoku board */
let sudokuBoard = document.getElementById('board');
// styling classes for the sudoku board
let numClasses = ['tlcorner', 'top', 'trcorner', 'left', 'center', 'right', 'blcorner', 'bottom', 'brcorner']
/* Dynamic creation of board divs */
for (let squareRow = 0; squareRow < 3; squareRow++) {
    for (let squareColumn = 0; squareColumn < 3; squareColumn++) {
        const newDiv = document.createElement('div');
        newDiv.classList.add('square');
        for (let innerRow = 0; innerRow < 3; innerRow++) {
            for (let innerColumn = 0; innerColumn < 3; innerColumn++) {
                const numDiv = document.createElement('div');
                numDiv.classList.add('number');
                //Add the sudoku board styling classes
                numDiv.classList.add(numClasses[(innerRow * 3) + innerColumn]);
                // This line commentable. Used for troubleshooting
                numDiv.textContent = 1 + (innerRow * 3) + innerColumn; 
                // Setting cell rows and columns
                let row = innerRow + squareRow * 3;
                let column = innerColumn + squareColumn * 3;
                numDiv.dataset.row = row;
                numDiv.dataset.column = column;

                // TODO - make the board the same as the puzzle created
                // Currently just sets all squares as 1-9
                board[row][column].value = 1 + (innerRow * 3) + innerColumn;
                newDiv.appendChild(numDiv); // Append numDiv to newDiv
            }
        }
        sudokuBoard.appendChild(newDiv); // Append newDiv to sudokuBoard
    }
}

// console.log(board); // Troubleshooting for dynamic creation

/* automate creation of buttons */
let buttons = document.getElementById('buttons');
for (let i = 1; i < 10; i++) {
    const newButton = document.createElement('button');
    newButton.type = 'button';
    newButton.textContent = i;
    buttons.appendChild(newButton);
}


/* Trigger event hookup code */
setupEventListeners(board);