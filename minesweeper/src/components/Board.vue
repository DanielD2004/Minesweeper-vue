<template>
    <div id="container">
        <div :id="level" class="board">
            <template v-for="row in minesweeperBoard">
                <template v-for="tile in row">
                    <button :disabled="tile.isDisabled" @click="dig(tile.x, tile.y)" @click.middle="flag(tile)">{{ display(tile) }}</button>
                </template>
            </template>
        </div>
    </div>
</template> 

<script setup>
    import { reactive } from 'vue';
    const props = defineProps(['level'])
    var maxSize = 0, bombChance = 0;
    
    
    // change size of grid and chance for a bomb to spawn
    switch (props.level){
        case 'easy':
            maxSize = 10;
            bombChance = 20;
            break;
        case 'medium':
            maxSize = 15;
            bombChance = 30;
            break;
        case 'hard':
            maxSize = 30;
            bombChance = 40;
            break;
    }

    //make board
    function initBoard(){
        var board = reactive([]);
        for (var i = 0; i < maxSize; i++){
            board.push([])
            for (var j = 0; j < maxSize; j++){
                var initializedTile = {nearbyBombs: 0, isFlagged: false, isRevealed: false, isBomb: false, y: j, x: i, isDisabled: false};
                board[i].push(initializedTile);
            }
        }
        return board;
    }

    // Using bombChance set by difficulty, randomly return true or false, indicating if tile will be a bomb
    function decideIfBomb(){
        var rando = Math.floor(Math.random() * 101);
        return rando <= bombChance ? true : false;
    }
    
    // Go through each tile, call helper function to decide if it will be a bomb
    function placeBombs(){
        for (var i = 0; i < maxSize; i++){
            for (var j = 0; j < maxSize; j++){
                minesweeperBoard[i][j].isBomb = decideIfBomb();
            }
        }
    }

    function checkIfTileIn(i, j){
        if (i < 0 || j < 0){
            return false;
        }
        if (i >= maxSize || j >= maxSize){
            return false;
        }
        return true;
    }

    function findBombs(){
        for (var i = 0; i < maxSize; i++){
            for (var j = 0; j < maxSize; j++){
                scanAroundTile(i, j);
            }
        }
    }

    function scanAroundTile(i, j){
        // Check Below
        var inOrOut = checkIfTileIn(i + 1, j);
        if (inOrOut == true){
            if (minesweeperBoard[i + 1][j].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Below to the right
        var inOrOut = checkIfTileIn(i + 1, j + 1);
        if (inOrOut == true){
            if (minesweeperBoard[i + 1][j + 1].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Below to the left
        var inOrOut = checkIfTileIn(i + 1, j - 1);
        if (inOrOut == true){
            if (minesweeperBoard[i + 1][j - 1].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Right
        var inOrOut = checkIfTileIn(i, j + 1);
        if (inOrOut == true){
            if (minesweeperBoard[i][j + 1].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Above to the right
        var inOrOut = checkIfTileIn(i - 1, j + 1);
        if (inOrOut == true){
            if (minesweeperBoard[i - 1][j + 1].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Above
        var inOrOut = checkIfTileIn(i - 1, j);
        if (inOrOut == true){
            if (minesweeperBoard[i - 1][j].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Above to the left
        var inOrOut = checkIfTileIn(i - 1, j - 1);
        if (inOrOut == true){
            if (minesweeperBoard[i - 1][j - 1].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Left
        var inOrOut = checkIfTileIn(i, j - 1);
        if (inOrOut == true){
            if (minesweeperBoard[i][j - 1].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }
    }

    function dig(x, y){
        console.log(x)
        console.log(y)
        console.log(minesweeperBoard)
        var square = minesweeperBoard[x][y];
        if (x < 0 || y < 0){
            return;
        }
        if (x > maxSize || y > maxSize){
            return;
        }
        if (square.isRevealed == true){
            return;
        }
        if (square.isFlagged == true){
            square.isFlagged = false;
            return;
        }
        if (square.isBomb){
            console.log("BOOM");
            return;
        }
        if (square.isBomb == false){
            square.isRevealed = true;
            square.isDisabled = true;
        }
        if (square.nearbyBombs == 0){
            dig(minesweeperBoard[x - 1][y - 1]);
            dig(minesweeperBoard[x][y - 1]);
            dig(minesweeperBoard[x + 1][y - 1]);
            dig(minesweeperBoard[x - 1][y]);
            dig(minesweeperBoard[x + 1][y]);
            dig(minesweeperBoard[x - 1][y + 1]);
            dig(minesweeperBoard[x][y + 1]);
            dig(minesweeperBoard[x + 1][y + 1]);
        }
    }

    function flag(tile){
        tile.isFlagged = true;
    }

    function display(tile){
        if (tile.isFlagged == true)
            return "FLAG"
        else if (tile.isRevealed == true)
            return tile.nearbyBombs;
        else
            return "X"
    }

    var minesweeperBoard = initBoard();
    placeBombs();
    findBombs();
    
</script>

<style scoped>

    button{
        width:50px;
        height:50px;
    }

    .container{
        width:100vw;
    }
    .board{
        margin-left:auto;
        margin-right:auto;
    }

    #easy{
        width:500px;
    }

    #medium{
        width:750px;
    }

    #hard{
        width:1500px;
    }
</style>