<script setup lang="ts">
import Button from 'primevue/button';
import FileUpload, { type FileUploadSelectEvent } from 'primevue/fileupload';
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
const { t } = useI18n();

function onSelect(event: FileUploadSelectEvent) {
  selectedFile.value = event.files[0] ?? null;
}

async function upload(strategyOverride?: ProcessingStrategy) {
  if (!selectedFile.value) {
    status.value = t('upload.chooseFileFirst');
    return;
  }

  const selectedStrategy = strategyOverride ?? strategy.value;
  const response = await uploadDocument(selectedFile.value, selectedStrategy);
  status.value = response.deduplicated
    ? t('upload.duplicate', {
        name: selectedFile.value.name,
        id: response.document_id,
      })
    : t('upload.uploaded', {
        name: selectedFile.value.name,
        id: response.document_id,
      });
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
            <label class="radio-row">
              <RadioButton v-model="strategy" input-id="scanner" value="scanner_ocr" />
              <span>{{ t('upload.scannerOcr') }}</span>
            </label>
            <label class="radio-row">
              <RadioButton v-model="strategy" input-id="ocr-model" value="ocr_model" />
              <span>{{ t('upload.ocrModel') }}</span>
            </label>
            <Button :label="t('upload.upload')" @click="upload()" />
          </div>
        </TabPanel>

        <TabPanel value="images">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload :choose-label="t('upload.chooseImage')" @select="onSelect" />
            <Button :label="t('upload.uploadWithOcr')" @click="upload('ocr_model')" />
          </div>
        </TabPanel>

        <TabPanel value="office">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload :choose-label="t('upload.chooseOffice')" @select="onSelect" />
            <Button :label="t('upload.uploadWithParser')" @click="upload('parser')" />
          </div>
        </TabPanel>

        <TabPanel value="text">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload :choose-label="t('upload.chooseText')" @select="onSelect" />
            <Button :label="t('upload.uploadText')" @click="upload('parser')" />
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>

    <p v-if="status" class="upload-status">{{ status }}</p>
  </main>
</template>

