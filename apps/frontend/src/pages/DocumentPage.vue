<script setup lang="ts">
import ProgressSpinner from 'primevue/progressspinner';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import { getDocumentMarkdown } from '../services/api';

const route = useRoute();
const markdown = ref('');
const loading = ref(true);

onMounted(async () => {
  markdown.value = await getDocumentMarkdown(String(route.params.id));
  loading.value = false;
});
</script>

<template>
  <main class="document-page">
    <ProgressSpinner v-if="loading" />
    <pre v-else class="markdown-reader">{{ markdown }}</pre>
  </main>
</template>

