<script setup lang="ts">
import Button from 'primevue/button';
import FileUpload, { type FileUploadSelectEvent } from 'primevue/fileupload';
import ProgressBar from 'primevue/progressbar';
import RadioButton from 'primevue/radiobutton';
import Tab from 'primevue/tab';
import TabList from 'primevue/tablist';
import TabPanel from 'primevue/tabpanel';
import TabPanels from 'primevue/tabpanels';
import Tabs from 'primevue/tabs';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { uploadDocument, type ProcessingStrategy } from '../services/api';

const selectedFile = ref<File | null>(null);
const strategy = ref<ProcessingStrategy>('scanner_ocr');
const status = ref('');
const error = ref('');
const uploading = ref(false);
const uploadProgress = ref(0);
const uploadStage = ref('');
const { t } = useI18n();

function onSelect(event: FileUploadSelectEvent) {
  selectedFile.value = event.files[0] ?? null;
  status.value = '';
  error.value = '';
  uploadProgress.value = 0;
  uploadStage.value = '';
}

async function upload(strategyOverride?: ProcessingStrategy) {
  if (!selectedFile.value) {
    status.value = t('upload.chooseFileFirst');
    return;
  }

  try {
    uploading.value = true;
    error.value = '';
    status.value = '';
    uploadProgress.value = 0;
    uploadStage.value = t('upload.stages.uploading');

    const selectedStrategy = strategyOverride ?? strategy.value;
    const response = await uploadDocument(selectedFile.value, selectedStrategy, (progress) => {
      uploadProgress.value = progress;
      if (progress >= 100) {
        uploadStage.value = t('upload.stages.processing');
      }
    });

    uploadProgress.value = 100;
    uploadStage.value = t('upload.stages.done');
    status.value = response.deduplicated
      ? t('upload.duplicate', {
          name: selectedFile.value.name,
          id: response.document_id,
        })
      : t('upload.uploaded', {
          name: selectedFile.value.name,
          id: response.document_id,
        });
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : t('upload.failed');
    uploadStage.value = t('upload.stages.failed');
  } finally {
    uploading.value = false;
  }
}
</script>

<template>
  <main class="upload-page">
    <h1>{{ t('upload.title') }}</h1>

    <Tabs value="pdf">
      <TabList>
        <Tab value="pdf">{{ t('upload.tabs.pdf') }}</Tab>
        <Tab value="images">{{ t('upload.tabs.images') }}</Tab>
        <Tab value="office">{{ t('upload.tabs.office') }}</Tab>
        <Tab value="text">{{ t('upload.tabs.text') }}</Tab>
      </TabList>

      <TabPanels>
        <TabPanel value="pdf">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload :choose-label="t('upload.choosePdf')" @select="onSelect" />
            <div v-if="selectedFile" class="selected-file">
              {{ t('upload.selectedFile') }}: {{ selectedFile.name }}
            </div>
            <label class="radio-row">
              <RadioButton v-model="strategy" input-id="scanner" value="scanner_ocr" :disabled="uploading" />
              <span>{{ t('upload.scannerOcr') }}</span>
            </label>
            <label class="radio-row">
              <RadioButton v-model="strategy" input-id="ocr-model" value="ocr_model" :disabled="uploading" />
              <span>{{ t('upload.ocrModel') }}</span>
            </label>
            <Button
              :disabled="uploading"
              :label="t('upload.upload')"
              :loading="uploading"
              @click="upload()"
            />
          </div>
        </TabPanel>

        <TabPanel value="images">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload :choose-label="t('upload.chooseImage')" @select="onSelect" />
            <div v-if="selectedFile" class="selected-file">
              {{ t('upload.selectedFile') }}: {{ selectedFile.name }}
            </div>
            <Button
              :disabled="uploading"
              :label="t('upload.uploadWithOcr')"
              :loading="uploading"
              @click="upload('ocr_model')"
            />
          </div>
        </TabPanel>

        <TabPanel value="office">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload :choose-label="t('upload.chooseOffice')" @select="onSelect" />
            <div v-if="selectedFile" class="selected-file">
              {{ t('upload.selectedFile') }}: {{ selectedFile.name }}
            </div>
            <Button
              :disabled="uploading"
              :label="t('upload.uploadWithParser')"
              :loading="uploading"
              @click="upload('parser')"
            />
          </div>
        </TabPanel>

        <TabPanel value="text">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload :choose-label="t('upload.chooseText')" @select="onSelect" />
            <div v-if="selectedFile" class="selected-file">
              {{ t('upload.selectedFile') }}: {{ selectedFile.name }}
            </div>
            <Button
              :disabled="uploading"
              :label="t('upload.uploadText')"
              :loading="uploading"
              @click="upload('parser')"
            />
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>

    <section v-if="uploading || uploadProgress > 0" class="upload-progress-card">
      <div class="progress-header">
        <span>{{ uploadStage }}</span>
        <strong>{{ uploadProgress }}%</strong>
      </div>
      <ProgressBar :value="uploadProgress" />
    </section>

    <p v-if="status" class="upload-status">{{ status }}</p>
    <p v-if="error" class="error-state">{{ error }}</p>
  </main>
</template>

