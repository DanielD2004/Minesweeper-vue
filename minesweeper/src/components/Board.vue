<template>
    <Modal :outcome="winLose" id="modal" v-show="displayModal"/>
    <div :class="blurPage" id="container">
        <div :id="level" class="board">
            <template v-for="row in minesweeperBoard">
                <template v-for="tile in row">
                    <button :class="tile.cssStyle" :disabled="tile.isDisabled" @click="dig(tile.x, tile.y)" @click.middle="flag(tile)">{{ display(tile) }}</button>
                </template>
            </template>
        </div>
    </div>
</template> 

<script setup>
    import Modal from './Modal.vue'
    import { reactive, ref } from 'vue';
    const props = defineProps(['level'])
    var winLose = ref('');
    var maxSize = 0, bombChance = 0, displayModal = false, blurPage = 'noBlur', count = 0, flagCount = 0, bombCount = 0;
    
    
    // change size of grid and chance for a bomb to spawn
    switch (props.level){
        case 'easy':
            maxSize = 10;
            bombChance = 10;
            break;
        case 'medium':
            maxSize = 15;
            bombChance = 50;
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
        return rando <= bombChance ? true : false;
    }
    
    // Go through each tile, call helper function to decide if it will be a bomb
    function placeBombs(x, y){
        for (var i = 0; i < maxSize; i++){
            for (var j = 0; j < maxSize; j++){
                if (x == i && y == j){
                    minesweeperBoard[i][j].isBomb == false;
                }
                else{
                    minesweeperBoard[i][j].isBomb = decideIfBomb();
                    if (minesweeperBoard[i][j].isBomb){
                        bombCount++;
                    }
                }
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
        // on first dig, place bombs, first tile will never be a bomb
        if (count == 0){
            count++;
            placeBombs(x, y);
            findBombs();
        }
        if (x < 0 || y < 0){
            return;
        }
        if (x > maxSize -1 || y > maxSize - 1){
            return;
        }
        var square = minesweeperBoard[x][y];
        if (square.isRevealed == true){
            return;
        }
        if (square.isFlagged == true){
            square.isFlagged = false;
            flagCount--;
            return;
        }
        if (square.isBomb){
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
            dig(x - 1, y - 1);
            dig(x, y - 1);
            dig(x + 1, y - 1);
            dig(x - 1, y);
            dig(x + 1, y);
            dig(x - 1, y + 1);
            dig(x, y + 1);
            dig(x + 1, y + 1);
        }
    }

    function flag(tile){
        tile.isFlagged = true;
        if (checkWinCon(tile)){
            winLose = 'win';
            displayModal = true;
            blurPage = 'blur';
            return;
        }
    }

    function checkWinCon(tile){
        // Check if all flagged tiles are also bombs
        if (tile.isBomb && tile.isFlagged){
            flagCount++;
        }
        if (flagCount == bombCount){
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
    // if (count != 0){
    //     while (true){
    //         if (bombCount - flagCount == 0){
    //             winLose = 'win';
    //             displayModal = true;
    //             blurPage = 'blur';
    //             break;
    //         }
    //     }
    // }
</script>

<style scoped>

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
        width:500px;
    }

    #medium{
        width:750px;
    }

    #hard{
        width:1250px;
    }

    #modal{
        margin-top:300px;
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