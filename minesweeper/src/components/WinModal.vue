<template>
    <div v-if="outcome=='win'">
        <h2 id="title">You Won!</h2>
        <h3>You Found All The Bombs!</h3>
    </div>
</template>

<script setup>
    const prop = defineProps(['outcome'])
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
</style>