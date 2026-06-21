<script setup lang="ts">
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import ProgressSpinner from 'primevue/progressspinner';
import { ref } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';

import { useSearchStore } from '../stores/searchStore';

const route = useRoute();
const router = useRouter();
const store = useSearchStore();
const query = ref(String(route.query.q ?? ''));

async function submitSearch() {
  if (!query.value.trim()) {
    return;
  }

  await router.replace({ path: '/', query: { q: query.value } });
  await store.search(query.value);
}

if (query.value) {
  void store.search(query.value);
}
</script>

<template>
  <main class="search-page">
    <section class="hero-search">
      <h1>LocaScanScribe.AI</h1>
      <form class="search-box" @submit.prevent="submitSearch">
        <InputText v-model="query" class="search-input" placeholder="Search local documents" />
        <Button label="Search" type="submit" />
      </form>
    </section>

    <section v-if="store.loading" class="loading-state">
      <ProgressSpinner />
    </section>

    <section v-else-if="store.error" class="error-state">
      {{ store.error }}
    </section>

    <section v-else class="results">
      <article v-for="item in store.results" :key="item.document_id" class="result-card">
        <RouterLink class="result-title" :to="item.url">{{ item.title }}</RouterLink>
        <div class="result-url">{{ item.url }}</div>
        <p v-for="snippet in item.snippets" :key="snippet.chunk_id" class="snippet">
          {{ snippet.phrase }}
        </p>
      </article>
    </section>
  </main>
</template>

