<template>
  <div class="font-chinese antialiased">
    <Navbar />
    <RouterView />
    <Footer />
  </div>
</template>
<script setup lang="ts">
import Navbar from "./components/layout/Navbar/index.vue";
import Footer from "./components/layout/Footer/index.vue";
</script>
