<template>
    <Modal :outcome="winLose" id="modal" v-show="displayModal"/>
    <div :class="blurPage" id="container">
        <div :id="props.level" class="board">
            <template v-for="row in minesweeperBoard">
                <template v-for="tile in row">
                    <button :class="tile.cssStyle" :disabled="tile.isDisabled" @click="dig(tile.x, tile.y)" @click.middle="flag(tile)">{{ display(tile) }}</button>
                </template>
            </template>
        </div>
    </div>
</template> 

<script setup>
    //is it better to have modal in board, or emit win/lose to app, and have modal in app
    import Modal from './Modal.vue'
    import { reactive, ref } from 'vue';
    const props = defineProps(['level'])
    var winLose = ref('');
    var maxSize = 0, bombChance = 0, displayModal = false, blurPage = 'noBlur', count = 0, flagCount = 0, bombCount = 0, flaggedBombsCount = 0;
    
    
    // change size of grid and chance for a bomb to spawn
    switch (props.level){
        case 'easy':
            maxSize = 8;
            bombChance = 10;
            break;
        case 'medium':
            maxSize = 12;
            bombChance = 15;
            break;
        case 'hard':
            maxSize = 25;
            bombChance = 40;
            break;
    }

    //make board
    function initBoard(){
        var board = reactive([]);
        for (var i = 0; i < maxSize; i++){
            board.push([])
            for (var j = 0; j < maxSize; j++){
                var initializedTile = {nearbyBombs: 0, isFlagged: false, isRevealed: false, isBomb: false, y: j, x: i, isDisabled: false, cssStyle: 'notShown'};
                board[i].push(initializedTile);
            }
        }
        return board;
    }

    // Using bombChance set by difficulty, randomly return true or false, indicating if tile will be a bomb
    function decideIfBomb(){
        var rando = Math.floor(Math.random() * 101);
        return rando <= bombChance;
    }
    
    // Go through each tile, call helper function to decide if it will be a bomb
    function placeBombs(x, y){
        for (var i = 0; i < maxSize; i++){
            for (var j = 0; j < maxSize; j++){
                    if (i === x && j === y) {
                        minesweeperBoard[i][j].isBomb = false; 
                        continue;
                    }
                    minesweeperBoard[i][j].isBomb = decideIfBomb();
                    if (minesweeperBoard[i][j].isBomb){
                        bombCount++;
                    }
                }
            }
    findBombs();
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
        var tileInOrOut
        // Check Below
        tileInOrOut = checkIfTileIn(i + 1, j);
        if (tileInOrOut){
            if (minesweeperBoard[i + 1][j].isBomb){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Below to the right
         tileInOrOut = checkIfTileIn(i + 1, j + 1);
        if (tileInOrOut){
            if (minesweeperBoard[i + 1][j + 1].isBomb){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Below to the left
         tileInOrOut = checkIfTileIn(i + 1, j - 1);
        if (tileInOrOut){
            if (minesweeperBoard[i + 1][j - 1].isBomb){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Right
         tileInOrOut = checkIfTileIn(i, j + 1);
        if (tileInOrOut){
            if (minesweeperBoard[i][j + 1].isBomb){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Above to the right
         tileInOrOut = checkIfTileIn(i - 1, j + 1);
        if (tileInOrOut){
            if (minesweeperBoard[i - 1][j + 1].isBomb){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Above
         tileInOrOut = checkIfTileIn(i - 1, j);
        if (tileInOrOut){
            if (minesweeperBoard[i - 1][j].isBomb){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Above to the left
         tileInOrOut = checkIfTileIn(i - 1, j - 1);
        if (tileInOrOut){
            if (minesweeperBoard[i - 1][j - 1].isBomb){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }

        // Check Left
         tileInOrOut = checkIfTileIn(i, j - 1);
        if (tileInOrOut == true){
            if (minesweeperBoard[i][j - 1].isBomb == true){
                minesweeperBoard[i][j].nearbyBombs++;
            }
        }
    }

    function dig(x, y){
        // on first dig only, place bombs, first tile will never be a bomb
        if (count == 0){
            count++;
            placeBombs(x, y);
        }
        
        if (!checkIfTileIn(x, y)){
            return;
        }

        var square = minesweeperBoard[x][y];
        if (square.isRevealed == true){
            return;
        }
        if (square.isFlagged == true){
            return;
        }
        // Lose
        if (square.isBomb){
            disableButtons();
            winLose = 'lose';
            square.cssStyle = 'explode';
            displayModal = true;
            blurPage = 'blur';
            return;
        }
        if (square.isBomb == false){
            square.cssStyle = 'safe';
            square.isRevealed = true;
            square.isDisabled = true;
        }
        if (square.nearbyBombs == 0){
            dig(x, y - 1);
            dig(x - 1, y);
            dig(x + 1, y);
            dig(x, y + 1);
            dig(x+1, y+1);
            dig(x+1, y-1);
            dig(x-1, y+1);
            dig(x-1, y-1);
        }
    }

    function flag(tile){
        // Can't flag as first move, which would be considered a win
        if (count == 0){
            return;
        }
        
        // Already flagged, remove flag
        if (tile.isFlagged == true){
            tile.isFlagged = false;
            tile.cssStyle = "notshown"
            flagCount--;
            if (tile.isBomb){
                flaggedBombsCount--;
            }
            return;
        }
        else{
            tile.isFlagged = true;
            tile.cssStyle = "flagged"
            
            // Check if won everytime a tile is flagged
            if (checkWinCon(tile)){
                disableButtons();
                winLose = 'win';
                displayModal = true;
                blurPage = 'blur';
                return;
            }
        }
    }

    function disableButtons(){
        for (var i = 0; i < maxSize; i++){
            for (var j = 0; j < maxSize; j++){
                minesweeperBoard[i][j].isDisabled = true;
            }
        }
    }

    function checkWinCon(tile){
        // Check if all flagged tiles are also bombs
        if (tile.isFlagged){
            if (tile.isBomb){
                flaggedBombsCount++;
            }
            flagCount++;
        }
        if (flaggedBombsCount == bombCount && flagCount == bombCount){
            return true;
        }
        return false;
    }

    function display(tile){
        if (tile.isFlagged == true)
        return "FLAG"
        if (tile.nearbyBombs == 0 && tile.isRevealed == true){
            return "-";
        }
        else if (tile.isRevealed == true)
            return tile.nearbyBombs;
        else
            return "X"
    }

    var minesweeperBoard = initBoard();
</script>

<style scoped>

    .flagged {
        background-color: aqua;
    }
    .safe{
        background-color:lightgreen;
    }

    .explode{
        background-color: red;
    }

    button{
        color:black;
        font-weight: bold;
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
        width:400px;
    }

    #medium{
        width:600px;
    }

    #hard{
        width:1250px;
    }

    #modal{
        left: 0;
        right: 0;
        position:fixed;
        display:block;
        z-index:2;
        margin-left: 0 auto;
        margin-right: 0 auto;
    }

    .blur{
        -webkit-filter: blur(5px);
        -moz-filter: blur(5px);
        -o-filter: blur(5px);
        -ms-filter: blur(5px);
        filter: blur(5px);
    }
</style>