<script setup>
    import Header from './components/Header.vue'
    import Board from './components/Board.vue'
    import { ref } from 'vue'
    const diff = ref('');
</script>

<template>
    <Header @changeDifficulty="(difficulty) => diff = difficulty"/>
    {{ diff }} 
    <Board v-if="diff != ''" :level='diff' />
</template>

<style scoped>

</style>
