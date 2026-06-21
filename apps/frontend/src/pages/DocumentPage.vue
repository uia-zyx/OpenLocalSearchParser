<script setup lang="ts">
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import { computed } from 'vue';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import { getDocumentMarkdown, getOriginalDocumentUrl } from '../services/api';

const route = useRoute();
const documentId = computed(() => String(route.params.id));
const markdown = ref('');
const loading = ref(true);
const originalUrl = computed(() => getOriginalDocumentUrl(documentId.value));

onMounted(async () => {
  markdown.value = await getDocumentMarkdown(documentId.value);
  loading.value = false;
});
</script>

<template>
  <main class="document-page">
    <ProgressSpinner v-if="loading" />
    <section v-else>
      <div class="document-actions">
        <h1>Recognized Document</h1>
        <a :href="originalUrl" download>
          <Button label="Download original" icon="pi pi-download" />
        </a>
      </div>

      <pre class="markdown-reader">{{ markdown }}</pre>
    </section>
  </main>
</template>

