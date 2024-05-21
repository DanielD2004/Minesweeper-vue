<template>
    <div id="lose" v-if="props.outcome == 'lose'">
        <h2 id="title">You lost!</h2>
        <h3>You tried to dig up a bomb..</h3>
    </div>
    <div id="win" v-if="props.outcome == 'win'">
        <h2 id="title">You Won!</h2>
        <h3>You Found All The Bombs</h3>
    </div>
</template>

<script setup>
    const props = defineProps(['outcome'])
</script>

<style scoped>
    div {
        background-color: white;
        border:2px solid black;
        text-align:center;
        width:50vw;
        margin-left:auto;
        margin-right:auto;
    }

    #lose{
        z-index:1;
    }

    #win{
        z-index:2;
    }
</style>