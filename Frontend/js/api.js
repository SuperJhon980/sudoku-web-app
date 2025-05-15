export async function validateBoard(board) {
    const response = await fetch("http://127.0.0.1:8000/check-board", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ board: board })
    });

    const result = await response.json();
    console.log("Valid board?", result.valid);
}

export async function validateMove(board, row, column){
    const response = await fetch("http://127.0.0.1:8000/check-move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ board, row, column })
    });

    const result = await response.json();
    console.log("Valid move?", result.valid);
}