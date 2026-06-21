<script setup lang="ts">
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { RouterLink } from 'vue-router';

import {
  deleteDocument,
  getOriginalDocumentUrl,
  listDocuments,
  updateDocumentTitle,
  type DocumentListItem,
} from '../services/api';

const { t } = useI18n();
const documents = ref<DocumentListItem[]>([]);
const loading = ref(true);
const error = ref('');
const editingId = ref<string | null>(null);
const editingTitle = ref('');

async function loadDocuments() {
  try {
    loading.value = true;
    documents.value = await listDocuments();
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : t('documents.loadFailed');
  } finally {
    loading.value = false;
  }
}

function startEdit(document: DocumentListItem) {
  editingId.value = document.id;
  editingTitle.value = document.title;
}

function cancelEdit() {
  editingId.value = null;
  editingTitle.value = '';
}

async function saveTitle(document: DocumentListItem) {
  const nextTitle = editingTitle.value.trim();
  if (!nextTitle) {
    return;
  }

  const updatedDocument = await updateDocumentTitle(document.id, nextTitle);
  documents.value = documents.value.map((item) =>
    item.id === updatedDocument.id ? updatedDocument : item,
  );
  cancelEdit();
}

async function removeDocument(document: DocumentListItem) {
  if (!window.confirm(t('documents.confirmDelete', { title: document.title }))) {
    return;
  }

  await deleteDocument(document.id);
  documents.value = documents.value.filter((item) => item.id !== document.id);
}

onMounted(loadDocuments);
</script>

<template>
  <main class="documents-page">
    <div class="page-heading">
      <h1>{{ t('documents.title') }}</h1>
      <RouterLink to="/upload">
        <Button :label="t('documents.uploadNew')" icon="pi pi-plus" />
      </RouterLink>
    </div>

    <section v-if="loading" class="loading-state">
      <ProgressSpinner />
    </section>

    <section v-else-if="error" class="error-state">
      {{ error }}
    </section>

    <section v-else-if="documents.length === 0" class="empty-state">
      {{ t('documents.empty') }}
    </section>

    <section v-else class="documents-list">
      <article v-for="document in documents" :key="document.id" class="document-card">
        <div class="document-card-main">
          <div v-if="editingId === document.id" class="document-edit-form">
            <input v-model="editingTitle" class="document-title-input" />
            <Button :label="t('documents.save')" size="small" @click="saveTitle(document)" />
            <Button :label="t('documents.cancel')" size="small" text @click="cancelEdit" />
          </div>
          <RouterLink v-else class="result-title" :to="`/documents/${document.id}`">
            {{ document.title }}
          </RouterLink>
          <div class="document-meta">
            {{ document.original_filename }} · {{ document.mime_type }} · {{ document.status }}
          </div>
        </div>

        <div class="document-card-actions">
          <RouterLink :to="`/documents/${document.id}`">
            <Button :label="t('documents.openRecognized')" text />
          </RouterLink>
          <Button
            v-if="editingId !== document.id"
            :label="t('documents.rename')"
            icon="pi pi-pencil"
            text
            @click="startEdit(document)"
          />
          <Button
            :label="t('documents.delete')"
            icon="pi pi-trash"
            severity="danger"
            text
            @click="removeDocument(document)"
          />
          <a :href="getOriginalDocumentUrl(document.id)" :download="document.original_filename">
            <Button :label="t('documents.downloadOriginal')" icon="pi pi-download" text />
          </a>
        </div>
      </article>
    </section>
  </main>
</template>

