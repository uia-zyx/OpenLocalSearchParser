<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="app-shell">
    <header class="top-nav">
      <RouterLink class="brand" to="/">LocaScanScribe.AI</RouterLink>
      <nav>
        <RouterLink to="/">Search</RouterLink>
        <RouterLink to="/upload">Upload</RouterLink>
      </nav>
    </header>

    <RouterView />
  </div>
</template>

