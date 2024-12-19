<template>
    <div id="header-wrapper">
        <div id="difficulty">
            <button :disabled='isDisabled' @click="$emit('changeDifficulty', 'easy'); disableButton();" id="easy">EASY</button>
            <button :disabled='isDisabled' @click="$emit('changeDifficulty', 'medium'); disableButton();" id="medium">MEDIUM</button>
            <!-- <button @click="$emit('changeDifficulty', 'hard')" id="hard">Hard</button>   -->
        </div>

        <div id="title">Minesweeper</div>

        <div id="aboutMe">
            Daniel Duclos
            <a target="_blank" href="https://github.com/DanielD2004">
                <button id="github">github</button>
            </a>
        </div>
    </div> 
</template>

<script setup>
    import { ref } from 'vue';

    const isDisabled = ref(false);

    function disableButton(){
        isDisabled.value = true;
    }
</script>

<style scoped>

    #aboutMe button{
        margin-left:10px;
    }

    #title{
        font-size:20px;
        font-weight:bolder;
        margin-left:auto;
        margin-right:auto;
    }
    #header-wrapper{
        border-bottom:2px solid grey;
        padding-bottom: 10px;
        margin-bottom:20px;
        display:flex;
    }

    #difficulty{
        display:flex;
    }

    button{
        margin-right:20px;
    }
</style>
