document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const keyboard = document.getElementById('keyboard');
    let secretWord = WORDS[Math.floor(Math.random() * WORDS.length)];
    let currentRow = 0;
    let currentCol = 0;
    let guess = "";

    // Create the game board
    for (let i = 0; i < 30; i++) {
        const tile = document.createElement('div');
        tile.classList.add('tile');
        gameBoard.appendChild(tile);
    }

    // Create the keyboard
    const keys = "QWERTYUIOPASDFGHJKLZXCVBNM".split('');
    keys.forEach(key => {
        const keyElement = document.createElement('button');
        keyElement.classList.add('key');
        keyElement.textContent = key;
        keyElement.addEventListener('click', () => handleKeyPress(key));
        keyboard.appendChild(keyElement);
    });

    function handleKeyPress(key) {
        if (currentCol < 5) {
            guess += key;
            const tile = gameBoard.children[currentRow * 5 + currentCol];
            tile.textContent = key;
            currentCol++;
        }
    }

    function submitGuess() {
        if (currentCol === 5) {
            // Logic to check the guess will go here
            currentRow++;
            currentCol = 0;
            guess = "";
        }
    }

    const enterKey = document.createElement('button');
    enterKey.classList.add('key');
    enterKey.textContent = 'Enter';
    enterKey.addEventListener('click', submitGuess);
    keyboard.appendChild(enterKey);
});
