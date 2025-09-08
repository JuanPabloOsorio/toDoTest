<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import BoardView from './views/BoardView.vue';
</script>

<template>
<!---
  <header>
    
    <div class="wrapper">

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>
  
  <RouterView />-->
  <main>
    <BoardView></BoardView>
  </main>
  

</template>

<style scoped>



</style>
