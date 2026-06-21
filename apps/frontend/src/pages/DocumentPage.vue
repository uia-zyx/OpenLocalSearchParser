<script setup lang="ts">
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import { computed } from 'vue';
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';

import { getDocumentMarkdown, getOriginalDocumentUrl } from '../services/api';

const route = useRoute();
const { t } = useI18n();
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
        <h1>{{ t('document.recognized') }}</h1>
        <a :href="originalUrl" download>
          <Button :label="t('document.downloadOriginal')" icon="pi pi-download" />
        </a>
      </div>

      <pre class="markdown-reader">{{ markdown }}</pre>
    </section>
  </main>
</template>

