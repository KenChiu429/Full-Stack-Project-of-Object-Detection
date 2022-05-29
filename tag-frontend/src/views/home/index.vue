<template>
  <div>
    <div class="flex w-full justify-center">
      <Menu />
    </div>
    <div class="min-h-screen w-full">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import Menu from "./components/Menu.vue";
</script>
<style scoped></style>
