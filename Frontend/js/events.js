import { validateBoard, validateMove } from './api.js';

/* event listeners */
export function setupEventListeners(board) {
    document.querySelectorAll('div.number').forEach(function (elt) {
        elt.addEventListener('click', handleCellClick)
    });
    document.querySelectorAll('#buttons button').forEach(function (elt) {
        elt.addEventListener('click', () => {
            const text = elt.textContent;
            handleButton(text, board);
        });
    });
}
/*
    This function handles button presses
    Buttons could be 1-9 or 'Undo' or 'Delete'
*/
async function handleButton(text, board) {
    let num = Number(text);
    let activeCell = document.querySelector('div.active');
    let row = parseInt(activeCell.dataset.row, 10);
    let column = parseInt(activeCell.dataset.column, 10);
    if (Number.isInteger(num)) {
        // TODO - prevent from overwriting given numbers
        activeCell.textContent = num; // update
        board[row][column].value = num;
        //Check if move is valid and update highlights accordingly
        if (await validateMove(board, row, column)) {
            // Orange
            highlightBrothers(num);
        } else {
            // Red
            highlightBrothers(num);
            highlightEnemies(activeCell);
        }

    } else if (text === "Undo") {
        // TODO - Have a history??
        validateBoard(board);
        console.log("not implemented yet: Undo");
        // next line probably wrong
        highlightBrothers(activeCell.textContent); // Update based on the old active cell
    } else if (text === "Delete") {
        // TODO - prevent from overwriting given numbers
        activeCell.textContent = ""; // delete
        highlightBrothers(-1); // clear out the equality cells
        board[row][column].value = 0;
    }
    //console.log(board); // Troubleshooting
}
/*
    This function highlights clicked cell and unhighlights old cell
*/
function handleCellClick(event) {
    /* Get the active cell and the target to edit their classes */
    let target = event.target;
    let activeCell = document.querySelector('div.active');
    let num = target.textContent;
    highlightNeighbors(target);
    highlightBrothers(num);
    if (activeCell) {
        activeCell.classList.remove('active');
    }
    target.classList.add('active');
}

/*
    This function highlights all the numbers in the sudoku which 
    Are the same number. Helps accessibility
*/
function highlightBrothers(num) {
    document.querySelectorAll('div.number').forEach(function (elt) {
        if (elt.textContent == num) {
            elt.classList.add('equality');
        } else {
            elt.classList.remove('equality');
        }
    });
}

/*
    This function highlights all the numbers in the sudoku which 
    Are the neighbors to the given number. Helps accessibility
*/
function highlightNeighbors(cell) {
    let neighbors = getNeighbors(cell);
    document.querySelectorAll('.number').forEach(neighbor => {
        if (neighbors.includes(neighbor)) {
            neighbor.classList.add('neighbor');
        } else {
            neighbor.classList.remove('neighbor');
        }
    });
    //console.log(cellRow);
    //console.log(cellColumn);
}

/*
    This function highlights all the numbers in the sudoku which 
    Are the neighbors to the given number. Helps accessibility
*/
function highlightEnemies(cell) {
    let neighbors = getNeighbors(cell);
    document.querySelectorAll('.number').forEach(neighbor => {
            if (neighbors.includes(neighbor) && cell.textContent === neighbor.textContent) {
                neighbor.classList.add('invalid');
            } else {
                neighbor.classList.remove('invalid');
            }
    });
    //console.log(cellRow);
    //console.log(cellColumn);
}


/*
    This function gets an array of all the neighbors of a given cell
    neighbors are in-row or in-column or in-square neighboring cells
*/
function getNeighbors(cell) {
    let cellRow = cell.dataset.row;
    let cellColumn = cell.dataset.column;
    let squareRow = Math.trunc(parseInt(cellRow) / 3) * 3;
    let squareColumn = Math.trunc(parseInt(cellColumn) / 3) * 3;
    let squareRows = [];
    let squareColumns = [];
    for (let i = 0; i < 3; i++) {
        squareRows[i] = (squareRow + i).toString();
        squareColumns[i] = (squareColumn + i).toString();
    }
    let neighbors = Array.from(document.querySelectorAll('.number')).filter(otherCell =>
        otherCell.dataset.row === cellRow || otherCell.dataset.column === cellColumn ||
        (squareRows.includes(otherCell.dataset.row) && squareColumns.includes(otherCell.dataset.column))
    );
    return neighbors;
}