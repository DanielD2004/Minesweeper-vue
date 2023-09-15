<template>
    <div>
        <div :id="level" class="board">
            <wrapper v-for="row in board">
                <wrapper v-for="tile in row">
                    <button>{{ tile }}</button>
                </wrapper>
            </wrapper>
        </div>
    </div>
</template> 

<script setup>
    const props = defineProps(['level'])
    var maxSize = 0, bombChance = 0;
    var board = []
    
    switch (props.level){
        case 'easy':
            maxSize = 10;
            bombChance = 20;
            break;
        case 'medium':
            maxSize = 20;
            bombChance = 30;
            break;
        case 'hard':
            maxSize = 30;
            bombChance = 40;
            break;
    }

    //make board
    for (var i = 0; i < maxSize; i++){
        board.push([])
        for (var j = 1; j <= maxSize; j++){
            board[i].push(j);
        }
    }
    console.log(board);
</script>

<style scoped>

    .board{
        margin-left:auto;
        margin-right:auto;
    }

    #easy{
        width:220px;
    }

    #medium{
        width:480px;
    }

    #hard{
        width:760px;
    }
</style>